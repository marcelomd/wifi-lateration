/*
 * trace.h
 */

#ifndef __TRACE_H
#define __TRACE_H

// Trace levels.
typedef enum {
    TRACE_NONE = 0, // When we don't want to print.
    TRACE_ERROR,
    TRACE_WARNING,
    TRACE_INFO,
    TRACE_DEBUG,
} trace_level_t;

/* Initializes tracing functionality.
 */
void trace_init(void);

/* Closes tracing.
 */
void trace_close(void);

/* Trace levels <= Config.trace_level are printed.
 */
void trace(trace_level_t level, char* fmt, ...);

#endif // __TRACE_H
