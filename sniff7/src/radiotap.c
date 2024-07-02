/*
 * radiotap.c
 */

#include <stdio.h>

#include "radiotap.h"

/*****************************************************************************/

/* Extracts one little endian 16 bit integer.
 * __p:     Pointer to little endian 16 bit integer.
 * return:  Big endian 16 bit integer.
 */
#define EXTRACT_LE_16BITS(__p) \
    ((uint16_t)((uint16_t)*((const uint8_t *)(__p) + 1) << 8 | \
                (uint16_t)*((const uint8_t *)(__p) + 0)))

/* Checks if bit is set on bitmap field.
 * __p: Pointer to bitmap.
 * __f: Bit to check.
 * return:  True if bit is set. False if not.
 */
#define IS_PRESENT(__p,__f) ((__p) & (__f))

/*****************************************************************************/

// Radiotap field presence bitmap. Little endian.
enum ieee80211_radiotap_le_field {
    IEEE80211_RADIOTAP_TSFT              = 0x01000000,
    IEEE80211_RADIOTAP_FLAGS             = 0x02000000,
    IEEE80211_RADIOTAP_RATE              = 0x04000000,
    IEEE80211_RADIOTAP_CHANNEL           = 0x08000000,
    IEEE80211_RADIOTAP_FHSS              = 0x10000000,
    IEEE80211_RADIOTAP_DBM_ANTSIGNAL     = 0x20000000,
    IEEE80211_RADIOTAP_DBM_ANTNOISE      = 0x40000000,
    IEEE80211_RADIOTAP_LOCK_QUALITY      = 0x80000000,
    IEEE80211_RADIOTAP_TX_ATTENUATION    = 0x00010000,
    IEEE80211_RADIOTAP_DB_TX_ATTENUATION = 0x00020000,
    IEEE80211_RADIOTAP_DBM_TX_POWER      = 0x00040000,
    IEEE80211_RADIOTAP_ANTENNA           = 0x00080000,
    IEEE80211_RADIOTAP_DB_ANTSIGNAL      = 0x00100000,
    IEEE80211_RADIOTAP_DB_ANTNOISE       = 0x00200000,
    // Several other fields...
    IEEE80211_RADIOTAP_EXT               = 0x00000080,
};

/*****************************************************************************/

// Radiotap header format.
struct ieee80211_radiotap_header {
    uint8_t it_version;     // Radiotap header version.
    uint8_t it_pad;         // Header is padded.
    uint16_t it_len;        // Header size.
    uint32_t it_present;    // Field presence bitmap.
};

/*****************************************************************************/

int radiotap_get_signal(const uint8_t* packet, int length, int8_t* signal)
{
    struct ieee80211_radiotap_header* header;
    uint32_t len;
    int8_t* p;

    // we captured less than one full header.
    if (length < sizeof(struct ieee80211_radiotap_header))
        return -1;

    header = (struct ieee80211_radiotap_header*)packet;
    len = EXTRACT_LE_16BITS(&header->it_len);

    // We captured less than the announced size.
    if (length < len)
        return -1;

    // We only care about packets which inform signal strength.
    if (!IS_PRESENT(header->it_present, IEEE80211_RADIOTAP_DBM_ANTSIGNAL))
        return -2;

    p = ((int8_t*)header) + sizeof(struct ieee80211_radiotap_header);

    // Jump over other fields...
    if (header->it_present & IEEE80211_RADIOTAP_TSFT)
        p += 8; // TSFT is 64bits.

    if (IS_PRESENT(header->it_present, IEEE80211_RADIOTAP_FLAGS)) 
        p += 1; // FLAGS are 8 bits.

    // XXX: Bug here: The space for this flag is always there, even if
    // the header says it's not present.
    //if (IS_PRESENT(header->it_present, IEEE80211_RADIOTAP_RATE))
        p += 1; // RATE is 8 bits.

    if (IS_PRESENT(header->it_present, IEEE80211_RADIOTAP_CHANNEL))
        p += 2 * 2; // Channel is 2 * 16 bits.

    if (IS_PRESENT(header->it_present, IEEE80211_RADIOTAP_FHSS))
        p += 2 * 1; // FHSS is 2 * 8 bits.

    *signal = *p;

    return len;
}

/*****************************************************************************/
