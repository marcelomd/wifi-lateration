/*
 * trace.c
 */

#include <stdio.h>
#include <stdarg.h>
#include <syslog.h>

#include "config.h"
#include "trace.h"

/*****************************************************************************/

void trace_init(void)
{
    openlog("sniff7", LOG_PID | LOG_CONS | LOG_PERROR | LOG_NDELAY, LOG_USER);
}

/*****************************************************************************/

void trace_close(void)
{
    closelog();
}

/*****************************************************************************/

void trace(trace_level_t level, char* fmt, ...)
{
    if (level <= Config.trace_level) {
        va_list args;
        va_start(args, fmt);
        vsyslog(LOG_INFO, fmt, args);
        va_end(args);
    }
}

/*****************************************************************************/
