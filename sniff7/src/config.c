/*
 *  config.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "config.h"
#include "trace.h"
#include "test.h"

/*****************************************************************************/

#define LINE_SIZE (1024) // Max configuration line size.

/*****************************************************************************/

// Global Config object. Initialized to default configuration.
struct config_t Config = {
    .base_interface = "mesh0",
    .capture_interface = "mon0",
    .capture_filter = "(wlan subtype assoc-req) "
                      "or (wlan subtype reassoc-req) "
                      "or (wlan subtype probe-req) "
                      "or (wlan subtype atim) "
                      "or (wlan subtype ps-poll) "
                      "or (wlan subtype null) "
                      "and ((wlan dir nods) or (wlan dir tods))"
                      "",
    .capture_snap = 80,
    .buffer_size = 8,
    .report_interval = 5,
    .report_server_timeout = 5,
    .report_server = "http://floodcreek.herokuapp.com/reports",
    .trace_level = 0,
    .test_mode = 0,
};

/*****************************************************************************/

/* Transforms string to lowercase, in place.
 * *s:  String to transform.
 */
static void lowercase(char* s)
{
    while (*s++)
        if ((*s >= 'A') && (*s <= 'Z'))
            *s |= 0x20;
}

/*****************************************************************************/

/* Checks if character is whitespace.
 * *s:  Character to check.
 * return:  True if character is space.
 */
static int is_space(char* s)
{
    return ((*s == ' ')
            || (*s == '\n')
            || (*s == '\r')
            || (*s == '\t')
            || (*s == '\f')
            || (*s == '\v'));
}

/*****************************************************************************/

/* Strip whitespace chars off end of given string, in place. 
 * *s:  String to work on.
 * return: s.
 */
static char* strip(char* s)
{
    char* p = s + strlen(s);
    while (p > s && is_space(--p))
        *p = '\0';
    return s;
}

/*****************************************************************************/

/* Skips whitespace until first character.
 * *s: String to work on.
 * return: Pointer to first non-whitespace char in given string.
 */
static char* skip(char* s)
{
    while (*s && is_space(s))
        s++;
    return s;
}

/*****************************************************************************/

/* Strips comments off end of string, in place.
 * *s:  String to work on.
 */
static void strip_comment(char* s)
{
    while (*s) {
        if (*s == '#') {
            *s = '\0';
        }
        s++;
    }
}

/*****************************************************************************/

/* Stores given configuration into Config object.
 * *key:    Configuration field.
 * *value:  Value to apply to given key.
 * return:  0 on success. Error code otherwise.
 */
static int handle_config(char* key, char* value)
{
    char* v = strdup(value);

    if (v == NULL) {
        trace(TRACE_ERROR, "Config> Memory error.\n");
        return -1;
    }

    lowercase(key);

    if (!strcmp("base_interface", key)) {
        Config.base_interface = v;
    }
    else if (!strcmp("capture_interface", key)) {
        Config.capture_interface = v;
    }
    else if (!strcmp("capture_filter", key)) {
        Config.capture_filter = v;
    }
    else if (!strcmp("capture_snap", key)) {
        Config.capture_snap = atoi(v);
    }
    else if (!strcmp("buffer_size", key)) {
        Config.buffer_size = atoi(v);
    }
    else if (!strcmp("report_interval", key)) {
        Config.report_interval = atoi(v);
    }
    else if (!strcmp("report_server_timeout", key)) {
        Config.report_server_timeout = atoi(v);
    }
    else if (!strcmp("report_server", key)) {
        Config.report_server = v;
    }
    else if (!strcmp("trace_level", key)) {
        Config.trace_level = atoi(v);
    }
    else if (!strcmp("test_mode", key)) {
        Config.test_mode = atoi(v);
    }

    return 0;
}

/*****************************************************************************/

/* Parse a config file and calls and store its contents on Config object..
 * *file:   Open file handle to read config from.
 * return:  0 on success. Error code if error.
 */
static int parse_config(FILE* file)
{
    int n = 0;
    char line[LINE_SIZE];
    char* key;
    char* value;
    char* start;

    while (fgets(line, LINE_SIZE, file) != NULL) {
        n++;
        strip_comment(line);
        start = skip(strip(line));

        if (!start || !strlen(start))
            continue;

        key = strtok(start, "=");
        if (!key) {
            trace(TRACE_ERROR, "Config> Error parsing line %d\n", n);
            return -1;
        }
        key = strip(key);

        value = strtok(NULL, "=");
        if (value == NULL) {
            trace(TRACE_ERROR, "Config> Error parsing line %d\n", n);
            return -1;
        }
        value = skip(strip(value));

        if(handle_config(key, value)) {
            trace(TRACE_ERROR, "Config> Error parsing line %d\n", n);
            return -1;
        }
    }

    return 0;
}

/*****************************************************************************/

/* Obtains MAC address from first ethernet interface then store it on Config
 * object. We use this to uniquely identify this device.
 * return: 0 on success. Error code if error.
 */
static int get_local_mac(void)
{
    int i;
    char* start;
    char* end;
    char line[18];
    FILE* file = fopen("/sys/class/net/eth0/address", "r");

    if (!file)
        return -1;

    if(!fgets(line, sizeof(line), file))
        return -1;
    fclose(file);

    start = line;

    for (i = 0; i <= 6; i++) {
        Config.mac[i] = strtol(start, &end, 16);
        start = end + 1;
        if (errno == ERANGE)
            return -1;
    }

    return 0;
}

/*****************************************************************************/

int config_init(char* filename)
{
    int r;
    FILE* f = fopen(filename, "r");

    trace(TRACE_INFO, "Config> Reading from %s\n", filename);
    if (!f) {
        trace(TRACE_ERROR, "Config> Error: Unable to open file\n");
        return -1;
    }
    r = parse_config(f);
    fclose(f);
    if (r)
        return r;

    r = get_local_mac();

    trace(TRACE_INFO, "Config> Done\n");
    return r;
}

/*****************************************************************************/
