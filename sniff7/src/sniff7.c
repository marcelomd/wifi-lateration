/*
 * sniff7.c
 */

#include <stdio.h>
#include <stdlib.h> 
#include <unistd.h>
#include <signal.h>

#include "config.h"
#include "trace.h"
#include "list.h"
#include "sniffer.h"
#include "reporter.h"
#include "watchdog.h"

/*****************************************************************************/

/* Closes everything as cleanly as possible.
 */
static void signal_handler(int signum)
{
    trace(TRACE_ERROR, "(%d) Abort!\n\n", signum);
    sniffer_stop();
    reporter_stop();
    watchdog_stop();
    trace_close();
    exit(0);
}

/*****************************************************************************/

/* Prints running configuration to stdout.
 */
static void splash()
{
    trace(TRACE_INFO, "\n----- Sniff7 -----\n");

    trace(TRACE_INFO, " Local MAC address: %02x:%02x:%02x:%02x:%02x:%02x\n",
            Config.mac[0], Config.mac[1], Config.mac[2],
            Config.mac[3], Config.mac[4], Config.mac[5]);
    // ip
    trace(TRACE_INFO, "    Base interface: %s\n", Config.base_interface);
    trace(TRACE_INFO, " Capture interface: %s\n", Config.capture_interface);
    trace(TRACE_INFO, "    Capture filter: %s\n", Config.capture_filter);
    trace(TRACE_INFO, "      Capture snap: %d\n", Config.capture_snap);
    trace(TRACE_INFO, "       Buffer size: %d\n", Config.buffer_size);
    trace(TRACE_INFO, "      Reporting to: %s\n", Config.report_server);
    trace(TRACE_INFO, "   Report interval: %ds\n", Config.report_interval);
    trace(TRACE_INFO, "    Server timeout: %ds\n", Config.report_server_timeout);
    trace(TRACE_INFO, "       Trace level: %d\n", Config.trace_level);
    trace(TRACE_INFO, "         Test mode: %d\n", Config.test_mode);

    trace(TRACE_INFO, "\n");
}

/*****************************************************************************/

int main(int argc, char **argv)
{
    char* config_file;

    if (argc == 1)
        config_file = NULL;
    else if (argc == 2)
        config_file = argv[1];
    else {
        trace(TRACE_INFO, "Too many arguments.");
        exit(EXIT_FAILURE);
    }

    trace_init();

    if (config_init(config_file))
        exit(EXIT_FAILURE);

    splash();

    signal(SIGINT, signal_handler);     // 2
    signal(SIGKILL, signal_handler);    // 9
    signal(SIGTERM, signal_handler);    // 15
    signal(SIGSTOP, signal_handler);    // 17
    signal(SIGSEGV, signal_handler);    // 11

    if (watchdog_start()) {
        trace(TRACE_ERROR, "Error running watchdog.");
        exit(EXIT_FAILURE);
    }
    if (list_init()) {
        trace(TRACE_ERROR, "Error initializing list.");
        exit(EXIT_FAILURE);
    }
    if (reporter_start()) {
        trace(TRACE_ERROR, "Error running reporter.");
        exit(EXIT_FAILURE);
    }
    if (sniffer_start()) {
        trace(TRACE_ERROR, "Error running sniffer.");
        exit(EXIT_FAILURE);
    }

    while(1)
        sleep(120);

    exit(0);
}

/*****************************************************************************/
