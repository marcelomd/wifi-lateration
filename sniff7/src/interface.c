/*
 * interface.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <linux/if.h>

#include "config.h"
#include "trace.h"
#include "interface.h"

/*****************************************************************************/

static char* base;
static char* monitor;

/*****************************************************************************/

/* Verifies if the monitor interface exists.
 * return: 1 if it exists, 0 if not.
 */
static int monitor_exists(void)
{
    struct stat st;
    char path[32];
    sprintf(path, "/sys/class/net/%s/", monitor);
    if (stat(path, &st))
        return 0;
    return 1;
}

/*****************************************************************************/

/* Creates monitor interface.
 * return: 0.
 */
static int monitor_create(void)
{
    char cmd[256];
    sprintf(cmd, "iw %s interface add %s type monitor flags none", base, monitor);
    system(cmd);
    return 0;
}

/*****************************************************************************/

/* Retrieves flags from interface.
 * fd: Dummy file descriptor.
 * *name: Interface to operate on.
 * *flags: Pointer to receive flags bitmap.
 * return: 0 on success; -1 on error.
 */
static int get_flags(int fd, char* name, short* flags)
{
    struct ifreq ifr;
    memset(&ifr, 0, sizeof(struct ifreq));
    strncpy(ifr.ifr_name, name, IFNAMSIZ);
    if (ioctl(fd, SIOCGIFFLAGS, &ifr))
        return -1;
    *flags = ifr.ifr_flags;
    return 0;
}

/*****************************************************************************/

/* Sets interface flags.
 * fd: Dummy file descriptor.
 * *name: Interface to operate on.
 * flags: Flags bitmap to set.
 * return: 0 on success; -1 on error.
 */
static int set_flags(int fd, char* name, short flags)
{
    struct ifreq ifr;

    memset(&ifr, 0, sizeof(struct ifreq));
    strncpy(ifr.ifr_name, name, IFNAMSIZ);
    ifr.ifr_flags = flags;
    if (ioctl(fd, SIOCSIFFLAGS, &ifr))
        return -1;
    return 0;
}

/*****************************************************************************/

/* Verifies if monitor interface is up.
 * return: 1 if it is up; 0 if not.
 */
static int monitor_is_up(void)
{
    int fd = socket(PF_INET, SOCK_DGRAM, 0);
    short flags;
    int r;
    r = get_flags(fd, monitor, &flags);
    close(fd);
    if (r)
        return 0;
    return flags & IFF_UP;
}

/*****************************************************************************/

/* Brings monitor interface up.
 * return 0 on success; -1 on error.
 */
static int monitor_up(void)
{
    int fd = socket(PF_INET, SOCK_DGRAM, 0);
    short flags;
    if (get_flags(fd, monitor, &flags)) {
        close(fd);
        return -1;
    }
    if (set_flags(fd, monitor, flags | IFF_UP)) {
        close(fd);
        return -1;
    }
    close(fd);
    return 0;
}

/*****************************************************************************/

int interface_setup(void)
{
    base = Config.base_interface;
    monitor = Config.capture_interface;

    if (!monitor_exists()) {
        trace(TRACE_WARNING, "Interface> Creating capture interface.\n");
        if (monitor_create()) {
            trace(TRACE_WARNING, "Interface> Error creating capture interface.\n");
            return -1;
        }
    }

    if (!monitor_is_up()) {
        trace(TRACE_WARNING, "Interface> Bringing capture interface up.\n");
        if (monitor_up()) {
            trace(TRACE_WARNING, "Interface> Error bringing capture interface up.\n");
            return -1;
        }
    }

    trace(TRACE_WARNING, "Interface> OK.\n");

    return 0;
}

/*****************************************************************************/
