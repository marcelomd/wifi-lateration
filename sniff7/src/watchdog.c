/*
 * watchdog.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <sys/select.h>

#include "config.h"
#include "trace.h"
#include "watchdog.h"

/*****************************************************************************/

static int fd[2];   // Child/parent file descriptors.
static pid_t pid;   // Parent PID.

/*****************************************************************************/

void watchdog_ping(void)
{
    write(fd[1], "!", 2);
}

/*****************************************************************************/

/* Commits suicide.
 */
static void restart(void)
{
    trace(TRACE_ERROR, "Watchdog> Bite!\n");
    // Kinda hacky, but works.
    system("/etc/init.d/field7 restart &");
    kill(pid, SIGTERM);
    raise(SIGTERM);
}

/*****************************************************************************/

/* Watchdog main loop.
 * A reporter cycle takes at most 
 * report_interval + reporter_server_timeout seconds.
 * Three times that seems like a good interval.
 * If we're not pinged in this interval, stop application. Also try to restart.
 * If anything goes wrong, the external watchdog will know what to do.
 */
static void watchdog_loop(void)
{
    fd_set set;
    static struct timeval timeout;
    int ping;

    while (1) {
        FD_ZERO(&set);
        FD_SET(fd[0], &set);

        timeout.tv_sec = 3 * (Config.report_interval + Config.report_server_timeout);
        timeout.tv_usec = 0;

        ping = select(fd[0] + 1, &set, NULL, NULL, &timeout);

        if (ping == 0) {
            trace(TRACE_ERROR, "Watchdog> No activity.\n");
            break;
        }
        else if (ping < 0) {
            trace(TRACE_ERROR, "Watchdog> Select error.\n");
            break;
        }
        else {
            char buf[8];
            int r = read(fd[0], buf, sizeof(buf));

            if (r == 0) {
                trace(TRACE_ERROR, "Watchdog> Application died!.\n");
                break;
            }
        }
    }
    restart();
    return;
}


/*****************************************************************************/

int watchdog_start(void)
{
    pipe(fd);

    if ((pid = fork()) == -1) {
        trace(TRACE_ERROR, "Watchdog> Error forking\n");
        return -1;
    }
    else if (pid == 0) {
        // Application process is child.
        close(fd[0]);
        return 0;
    }
    else {
        // Watchdog process is parent.
        close(fd[1]);
        watchdog_loop();
        return -1;
    }
}

/*****************************************************************************/

void watchdog_stop(void)
{
    if (pid == 0)
        close(fd[1]);
    else
        close(fd[0]);
}

/*****************************************************************************/
