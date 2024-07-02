#!/bin/sh
# Installation script

VER=1
APP=sniff7
CONFIG=sniff7.cfg
STARTUP=startup.sh
WATCHDOG=watchdog.sh

SERVER=http://listenerservic.elasticbeanstalk.com/public
TMP_DIR=/tmp

INSTALLED_APP=/usr/bin/${APP}
INSTALLED_CONFIG=/etc/${CONFIG}
INSTALLED_STARTUP=/etc/init.d/field7
INSTALLED_WATCHDOG=/usr/bin/field7-watchdog
INSTALLED_WATCHDOG_LINK=/etc/cron.5mins/field7-watchdog

ETAG_FILE=/etc/${APP}.etag


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


download() {
    log "Downloading ${1}"
    wget --no-cache ${SERVER}/${1} -O ${TMP_DIR}/${1}
    verify ${TMP_DIR}/${1}
    log "Ok"
}


install() {
    log "Installing ${1} in ${2}"
    mv -f ${1} ${2}
    log "Done"
}


save_etag() {
    wget -S --spider ${SERVER}/custom.sh 2>&1 | \
        grep ETag | awk '{print $2}' | tr -cd '0-9A-z' > ${ETAG_FILE}
    verify ${ETAG_FILE}
    log "Etag: `cat ${ETAG_FILE}`"
}


##### MAIN
log "Running custom.sh"

# Remove old files
rm -f ${TMP_DIR}/${APP}
rm -f ${TMP_DIR}/${CONFIG}
rm -f ${TMP_DIR}/${STARTUP}
rm -f ${TMP_DIR}/${WATCHDOG}

# Clean slate
log "Uninstall"

rm -f ${INSTALLED_WATCHDOG}
killall -9 ${APP}

${INSTALLED_STARTUP} stop
${INSTALLED_STARTUP} disable

rm -f ${INSTALLED_APP}
rm -f ${INSTALLED_CONFIG}
rm -f ${INSTALLED_STARTUP}
rm -f ${ETAG_FILE}

# Download
download ${APP}
download ${CONFIG}
download ${STARTUP}
download ${WATCHDOG}

save_etag

# Install
install ${TMP_DIR}/${APP} ${INSTALLED_APP}
install ${TMP_DIR}/${CONFIG} ${INSTALLED_CONFIG}
install ${TMP_DIR}/${STARTUP} ${INSTALLED_STARTUP}
install ${TMP_DIR}/${WATCHDOG} ${INSTALLED_WATCHDOG}
ln -s ${INSTALLED_WATCHDOG} ${INSTALLED_WATCHDOG_LINK}

chmod +x ${INSTALLED_APP}
chmod +x ${INSTALLED_STARTUP}
chmod +x ${INSTALLED_WATCHDOG}

# Go!
log "Start!"
${INSTALLED_STARTUP} enable
${INSTALLED_STARTUP} start 5 &
