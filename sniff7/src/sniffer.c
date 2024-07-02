/*
 * sniffer.c
 */

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <pcap.h>

#include "config.h"
#include "trace.h"
#include "interface.h"
#include "list.h"
#include "radiotap.h"
#include "sniffer.h"
#include "test.h"

/*****************************************************************************/

// Standard IEEE 802.11 header.
struct ieee80211_header_t {
    uint16_t fc;        // Frame Control field. Little endian.
    uint16_t duration;  // Frame Duration/ID field. Little endian.
    uint8_t a1[6];      // First MAC address.
    uint8_t a2[6];      // Second MAC address.
    uint8_t a3[6];      // Third MAC address.
    uint16_t seq_ctrl;  // Sequence Control field. Little endian.
    uint8_t a4[6];      // Fourth MAC address
};

static pthread_t sniffer_thread;        // Sniffer thread handle.
static pcap_t *handle;                  // Packet capture handle.
static char errbuf[PCAP_ERRBUF_SIZE];   // Error buffer.
static char* device;                    // Capture interface.
static char* filter_exp;                // Filter expression.
static struct bpf_program fp;           // Compiled filter program (from expression).

/*****************************************************************************/

/* Pcap callback. This is called for every packet matching our filter
 * expression. Simply extract the Source MAC address from IEEE 802.11 header
 * and RSSI reading from Radiotap header then put into device list.
 * *args:   Not used.
 * *header: Pointer to pcap header. Contains info about the captured packet.
 * *packet: Pointer to start of packet.
 */
static void process_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
    int len;
    int8_t signal;
    struct ieee80211_header_t* h;
    entry_t entry;

    len = radiotap_get_signal(packet, header->caplen, &signal);
    if (len < 0)
        return;

    h = (struct ieee80211_header_t*)(packet + len);

    /* Data Frame - Address field contents
     *
     * ToDs | FromDS | Addr1 | Addr2 | Addr3 | Addr4
     *  0   |   0    | DA    | SA    | BSSID | n/a
     *  0   |   1    | DA    | BSSID | SA    | n/a
     *  1   |   0    | BSSID | SA    | DA    | n/a
     *  1   |   1    | RA    | TA    | DA    | SA
     *
     *  We're listening to ToDs/FromDS = 0/0 or 1/0,
     *  In both cases SA is the second address.
     */
    memcpy(entry.mac, h->a2, 6);
    entry.timestamp = time(NULL);
    entry.rssi = signal;

    list_lock();
    list_write(&entry);
    list_unlock();
}

/*****************************************************************************/

/* Initializes libpcap structures and opens interfaces for capture.
 */
static int pcap_init(void)
{
    device = Config.capture_interface;
    filter_exp = Config.capture_filter;

    // Open capture interface.
    handle = pcap_open_live(device, Config.capture_snap, 1, 1000, errbuf);
    if (handle == NULL) {
        trace(TRACE_ERROR, "Sniffer> Couldn't open device %s: %s\n", device, errbuf);
        return -1;
    }
    if (strlen(errbuf) > 0) {
        trace(TRACE_WARNING, "Sniffer> Warning: %s\n", errbuf);
        errbuf[0] = '\0'; // Reset buffer
    }


    // Make sure we're capturing on WIFI.
    if (pcap_datalink(handle) != DLT_IEEE802_11_RADIO) {
        trace(TRACE_ERROR, "Sniffer> %s is not WIFI\n", device);
        pcap_close(handle);
        return -1;
    }
    if (pcap_set_datalink(handle, DLT_IEEE802_11_RADIO) == -1) {
        pcap_perror(handle, "Sniffer> Error on pcap_set_datalink: ");
        pcap_close(handle);
        return -1;
    }


    // Compile the filter expression.
    if (pcap_compile(handle, &fp, filter_exp, 0, 0) == -1) {
        trace(TRACE_ERROR, "Sniffer> Couldn't parse filter %s: %s\n",
            filter_exp, pcap_geterr(handle));
        pcap_close(handle);
        return -1;
    }

    // Apply the compiled filter
    if (pcap_setfilter(handle, &fp) == -1) {
        trace(TRACE_ERROR, "Sniffer> Couldn't install filter %s: %s\n",
            filter_exp, pcap_geterr(handle));
        pcap_freecode(&fp);
        pcap_close(handle);
        return -1;
    }

    pcap_freecode(&fp);

    return 0;
}

/*****************************************************************************/

int sniffer_init(void)
{
    trace(TRACE_INFO, "Sniffer> Init\n");
    if (interface_setup())
        return -1;
    if (pcap_init())
        return -1;
    return 0;
}

/*****************************************************************************/

static void* sniffer_loop(void* arg)
{
    trace(TRACE_INFO, "Sniffer> Starting capture.\n");

    pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, NULL);

    while (1) {
        int r;

        // Try to (re)init.
        if (sniffer_init()) {
            sleep(30);
            continue;
        }

        r = pcap_loop(handle, -1, process_packet, NULL);
        pcap_close(handle);

        // Just get out if loop was broken.
        if (r == -2)
            break;

        trace(TRACE_ERROR, "Sniffer> Capture interrupted: %s\n", pcap_geterr(handle));
    }

    trace(TRACE_INFO, "Sniffer> Exit!");

    return NULL;
}

/*****************************************************************************/

int sniffer_start(void)
{
    if (Config.test_mode)
        return 0;

    return pthread_create(&sniffer_thread, NULL, sniffer_loop, NULL);
}

/*****************************************************************************/

void sniffer_stop(void)
{
    /* cleanup */
    pcap_breakloop(handle);
}

/*****************************************************************************/
