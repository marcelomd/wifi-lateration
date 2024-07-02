#! /bin/sh
# Watchdog script

APP=sniff7
INSTALLED_STARTUP=/etc/init.d/field7

SERVER=http://listenerservice.elasticbeanstalk.com/public

TMP_DIR=/tmp

ETAG_FILE=/etc/${APP}.etag
LOCAL_ETAG=1
SERVER_ETAG=2


log() {
    logger -t ${0##*/} ${1}
    echo ${1}
}


error() {
    logger -t ${0##*/} ${1}
    exit 1
}


verify() {
    [ ! -f ${1} ] && error "Missing file: ${1}"
}


local_etag() {
    LOCAL_ETAG=`cat ${ETAG_FILE}`
}


server_etag() {
    wget -S --spider ${SERVER}/custom.sh 2>&1 | \
        grep ETag | awk '{print $2}' | tr -cd '0-9A-z' > ${TMP_DIR}/etag
    SERVER_ETAG=`cat ${TMP_DIR}/etag`
}


update() {
    log "Updating..."
    wget ${SERVER}/custom.sh -O ${TMP_DIR}/custom.sh
    verify ${TMP_DIR}/custom.sh
    chmod +x ${TMP_DIR}/custom.sh
    ${TMP_DIR}/custom.sh
    exit 0
}


check_updates() {
    log "Check for updates"

    local_etag
    server_etag

    if [ ${LOCAL_ETAG} != ${SERVER_ETAG} ]; then
        update
    else
        log "Up to date =)"
    fi
}


check_app() {
    # Restart application if it's not running
    if [ -z "$(pgrep ${APP})" ]; then
        log "Starting ${APP}"
        ${INSTALLED_STARTUP} restart &
        logread > /root/wd.`date -I'seconds'`
    else
        log "${APP} running"
    fi
}


##### Main
check_updates
check_app
