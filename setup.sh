#!/bin/bash
BASEDIR=`pwd`

SNIFF7=${BASEDIR}/sniff7

OPENWRT=${BASEDIR}/openwrt
OPENWRT_REV=r31729



echo "----- sniff7 -----"
# Download OpenWRT
rm -rf ${OPENWRT}
svn co -r ${OPENWRT_REV} svn://svn.openwrt.org/openwrt/trunk ${OPENWRT}
${OPENWRT}/scripts/feeds update -a
${OPENWRT}/scripts/feeds install luci protobuf libprotobuf-c

# Patch OpenWRT
mkdir -p ${OPENWRT}/tools/bison/patches/
cp patches/100-fix-gets-removal.patch.bison ${OPENWRT}/tools/bison/patches/100-fix-gets-removal.patch
mkdir -p ${OPENWRT}/tools/m4/patches/
cp patches/100-fix-gets-removal.patch.m4 ${OPENWRT}/tools/m4/patches/100-fix-gets-removal.patch
#patch ${OPENWRT}/feeds/packages/libs/curl/Makefile curl-makefile.patch

ln -s ${SNIFF7} ${OPENWRT}/package/sniff7


