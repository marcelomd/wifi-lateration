/*
 * reporter.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <curl/curl.h>

#include "config.h"
#include "trace.h"
#include "list.h"
#include "watchdog.h"
#include "report.pb-c.h"
#include "reporter.h"
#include "test.h"

/*****************************************************************************/

static pthread_t reporter_thread;               // Thread handle.
static int break_loop;                          // Break from reporter thread.
static unsigned int pack_counter = 0;           // Report counter;
static Report report = REPORT__INIT;            // Main Protobuf Report object.
static Station** stations;                      // Collection of Protobuf Stations.
static void* report_buf;                        // Buffer holding the Report.
static unsigned int report_len;                 // Report's size.
static unsigned char report_mac[6];
static CURL* curl;                              // libcURL handle.
static CURLcode curl_ret;                       // libcURL error handle.
static struct curl_slist* curl_headers = NULL;  // libcURL connection headers.
static char curl_error[CURL_ERROR_SIZE];        // String to hold error message.

/*****************************************************************************/

/* Callback implementing cURL's write function. It does nothing and it's here
 * to prevent cURL from writing to stdout.
 */
static size_t write_callback(char* ptr, size_t size, size_t nmemb, void* userdata)
{
    return size * nmemb;
}

/*****************************************************************************/

/* Initializes report's protobuf structures.
 */
static int protobuf_init(void)
{
    int i;

    report.version = 2;
    report.mac.len = 6;
    report.mac.data = report_mac;
    memcpy(report.mac.data, Config.mac, 6);

    stations = malloc(sizeof(Station*) * Config.buffer_size);
    if (stations == NULL) {
        trace(TRACE_ERROR, "Reporter> Memory error: stations\n");
        return -1;
    }

    for (i = 0; i < Config.buffer_size; i++) {
        stations[i] = malloc(sizeof(Station));
        if (stations[i] == NULL) {
            trace(TRACE_ERROR, "Reporter> Memory error: stations[%d]\n", i);
            return -1;
        }

        station__init(stations[i]);
        stations[i]->mac.len = 6;
        stations[i]->mac.data = malloc(6);
        if (stations[i]->mac.data == NULL) {
            trace(TRACE_ERROR, "Reporter> Memory error: mac[%d]\n", i);
            return -1;
        }
    }

    return 0;
}

/*****************************************************************************/

/* Initializes libcurl for POSTing.
 */
static int curl_init(void)
{
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    curl_headers = curl_slist_append(curl_headers,
            "Content-Type: application/octet-stream");
    curl_easy_setopt(curl, CURLOPT_URL, Config.report_server);
    curl_easy_setopt(curl, CURLOPT_POST, 1);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, curl_headers);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, Config.report_server_timeout);
    curl_easy_setopt(curl, CURLOPT_ERRORBUFFER, curl_error);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    return 0;
}

/*****************************************************************************/

/* Initializes Reporter resources.
 */
int reporter_init(void)
{
    trace(TRACE_INFO, "Reporter> Init\n");
    break_loop = 0;
    pack_counter = 0;
    if (protobuf_init())
        return -1;
    if (curl_init())
        return -1;
    return 0;
}

/*****************************************************************************/

/* Reporter inner loop.
 * Every Config.report_interval seconds we lock the devices list and
 * prepare a report to send to our webapp.
 */
static void _reporter_loop(void)
{
    unsigned int delta;
    unsigned int next = time(NULL) + Config.report_interval;


    while (1) {
        int i = 0;
        entry_t entry;

        trace(TRACE_DEBUG, "Reporter> Wake up!\n");

        delta = next - time(NULL);
        if (delta > 0) {
            if (break_loop)
                return;
            sleep(delta);
            if (break_loop)
                return;
        }
        next = time(NULL) + Config.report_interval;

        watchdog_ping();

        if (Config.test_mode) {
            for (i = 0; i < Config.buffer_size; i++) {
                test_get_entry(&entry);
                memcpy(stations[i]->mac.data, entry.mac, 6);
                stations[i]->timestamp = entry.timestamp;
                stations[i]->rssi = entry.rssi;
                stations[i]->count = entry.count;
                trace(TRACE_DEBUG,
                        "Reporter> Test(%d) - ([%02x %02x %02x], %d, %d, %d)\n",
                        i,
                        stations[i]->mac.data[3],
                        stations[i]->mac.data[4],
                        stations[i]->mac.data[5],
                        stations[i]->timestamp,
                        stations[i]->rssi,
                        stations[i]->count);
            }
        }
        else {
            list_lock();
            while(!list_read(&entry)) {
                memcpy(stations[i]->mac.data, entry.mac, 6);
                stations[i]->timestamp = entry.timestamp;
                stations[i]->rssi = 0 - entry.rssi; // Pass along a positive number.
                stations[i]->count = entry.count;
                i++;
            }
            list_clear();
            list_unlock();
        }

        if (!i) {
            trace(TRACE_INFO, "Reporter> Nothing to send.\n");
            continue;
        }

        report.timestamp = (unsigned int)time(NULL);
        report.pack_counter = pack_counter++;
        report.n_stations = i;
        report.stations = stations;
        trace(TRACE_DEBUG, "> %d %d %d %d\n",
                i, report.timestamp, report.n_stations, report.pack_counter);
        report_len = report__get_packed_size(&report);
        report_buf = malloc(report_len);

        if (report_buf == NULL) {
            trace(TRACE_ERROR, "Reporter> malloc error\n");
            continue;
        }
        trace(TRACE_INFO, "Reporter> (%d) %d stations, %d bytes to send.\n",
                report.pack_counter, i, report_len);
        report__pack(&report, report_buf);

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, report_buf);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, report_len);
        curl_ret = curl_easy_perform(curl); /* post away! */

        if (!curl_ret)
            trace(TRACE_DEBUG, "Reporter> Done.\n");
        else
            trace(TRACE_ERROR, "Reporter> Error posting. (%d) %s\n", curl_ret, curl_error);
        free(report_buf);
    }
}

/*****************************************************************************/

/* Main reporter thread.
 * Handles errors and termination of Reporter.
 */
static void* reporter_loop(void* arg)
{
    trace(TRACE_INFO, "Reporter> Starting reporter.\n");

    if (reporter_init())
        return NULL;

    _reporter_loop();

    trace(TRACE_INFO, "Reporter> Exit!\n");
    return NULL;
}

/*****************************************************************************/

int reporter_start(void)
{
    return pthread_create(&reporter_thread, NULL, reporter_loop, NULL);
}

/*****************************************************************************/

void reporter_stop(void)
{
    break_loop = 1;
    pthread_join(reporter_thread, NULL);
}

/*****************************************************************************/
