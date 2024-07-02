#!/bin/sh /etc/rc.common
# Startup script

START=99
STOP=10

APP=sniff7
CONFIG=/etc/sniff7.cfg
INTERFACE=mesh0
MONITOR=mon0
DELAY=3


log() {
    logger -t ${0##*/} ${1}
    echo ${1}
}

error() {
    logger -t ${0##*/} ${1}
    exit 1
}


setup_interfaces() {
    STATUS=$(grep ${MONITOR} /proc/net/wireless | awk '{print $2}')
    if [ -z "${STATUS}" ]; then
        log "Creating ${MONITOR}"
        iw ${INTERFACE} interface add ${MONITOR} type monitor flags none
        log "OK"
    fi
    ifconfig ${MONITOR} up
}


restart() {
    stop
    start 1
}


start() {
    if [ -n "$1" ]; then
        D=${1}
    else
        D=${DELAY}
    fi

    log "Starting ${APP} in ${D}s"
    sleep ${D}
    setup_interfaces
    ${APP} ${CONFIG} 2>&1 &
}


stop() {
    log "Shutting down ${APP}"
    killall -9 ${APP}
}
