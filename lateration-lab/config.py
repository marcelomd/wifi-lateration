# encoding: utf-8

SITE_NAME = 'arezzo'

REFERENCE_DEVICE = 0x90187cc9e1c3

SECTORS = [                        #  Lower left,     Upper right 
    #{'id': 0,  'name': 'OUT', 'X': ((00.00, 00.00), (00.00, 00.00)},
    {'id': 1,  'name': 'AC1', 'X': (( 0.00, -1.72), ( 7.96,  4.65))},
    {'id': 2,  'name': 'AC2', 'X': (( 0.00,  4.65), ( 7.96, 11.02))},
    {'id': 3,  'name': 'AC3', 'X': (( 0.00, 11.02), ( 7.96, 15.41))},

    {'id': 4,  'name': 'SZ1', 'X': (( 7.96, -1.72), (16.08,  7.20))},
    {'id': 5,  'name': 'SZ2', 'X': ((16.08, -1.72), (24.20,  7.20))},
    {'id': 6,  'name': 'SZ3', 'X': ((16.08,  7.20), (24.20, 15.48))},
    {'id': 7,  'name': 'SZ4', 'X': (( 7.96,  7.20), (16.08, 15.48))},

    {'id': 8,  'name': 'AZ1', 'X': ((24.20,  0.00), (33.35,  8.09))},
    {'id': 9,  'name': 'AZ2', 'X': ((31.91,  0.00), (38.79,  8.09))},
    {'id': 10, 'name': 'AZ3', 'X': ((31.91,  8.09), (38.79, 16.75))},
    {'id': 11, 'name': 'AZ4', 'X': ((24.20,  8.09), (33.25, 16.75))},

    {'id': 12, 'name': 'CX',  'X': ((16.88, 15.47), (38.79, 22.42))},
]


NODES = {
        0xac86741082d8: {'index':  0, 'x': (00.00, 00.00)},
        0xac867410be10: {'index':  1, 'x': (12.42, 00.00)},
        0xac867410be28: {'index':  2, 'x': (24.77, 00.00)},
        0xac867410ea10: {'index':  3, 'x': (38.79, 00.00)},
        0xac86741ca318: {'index':  4, 'x': (00.00, 11.12)},
        0xac867410be08: {'index':  5, 'x': (12.42, 11.12)},
        0xac86741ca350: {'index':  6, 'x': (24.77, 11.12)},
        0xac86741082b0: {'index':  7, 'x': (38.79, 11.12)},
        0xac86741ca330: {'index':  8, 'x': (28.59, 22.42)},
        0x00180A81479E: {'index':  9, 'x': (28.59, 22.42)},
        0x00180A8147F4: {'index': 10, 'x': (28.59, 22.42)},
}

NODES_BY_INDEX ={
        0:  {'mac': 0xac86741082d8, 'x': (00.00, 00.00)},
        1:  {'mac': 0xac867410be10, 'x': (12.42, 00.00)},
        2:  {'mac': 0xac867410be28, 'x': (24.77, 00.00)},
        3:  {'mac': 0xac867410ea10, 'x': (38.79, 00.00)},
        4:  {'mac': 0xac86741ca318, 'x': (00.00, 11.12)},
        5:  {'mac': 0xac867410be08, 'x': (12.42, 11.12)},
        6:  {'mac': 0xac86741ca350, 'x': (24.77, 11.12)},
        7:  {'mac': 0xac86741082b0, 'x': (38.79, 11.12)},
        8:  {'mac': 0xac86741ca330, 'x': (28.59, 22.42)},
        9:  {'mac': 0x00180A81479E, 'x': (28.59, 22.42)},
        10: {'mac': 0x00180A8147F4, 'x': (28.59, 22.42)},
}


K = -8
N = 3.6


DATABASE = "dbLocalTrackingArezzo"
SERVER = "177.71.248.102"
USER = "localtrackingarezzoservico"
PASSWORD = "@ocivresozzeragnikcartlacol!"


FINGERPRINT = {
     1: {'sector':  1, 'time': (1405009255,1405009440)},
     2: {'sector':  1, 'time': (1405009449,1405009526)},
     3: {'sector':  1, 'time': (1405009540,1405009627)},
     4: {'sector':  1, 'time': (1405009638,1405009707)},
     5: {'sector':  1, 'time': (1405010837,1405010977)},

     6: {'sector':  2, 'time': (1405010375,1405010440)},
     7: {'sector':  2, 'time': (1405010448,1405010520)},
     8: {'sector':  2, 'time': (1405010282,1405010359)},
     9: {'sector':  2, 'time': (1405010735,1405010822)},
    10: {'sector':  2, 'time': (1405010200,1405010270)},

    11: {'sector':  3, 'time': (1405010578,1405010671)},
    12: {'sector':  3, 'time': (1405011000,1405011094)},
    13: {'sector':  3, 'time': (1405011103,1405011179)},
    14: {'sector':  3, 'time': (1405011187,1405011260)},
    15: {'sector':  3, 'time': (1405011270,1405011340)},

    18: {'sector':  4, 'time': (1405011649,1405011725)},
    19: {'sector':  4, 'time': (1405011734,1405011823)},
    20: {'sector':  4, 'time': (1405011837,1405011916)},
    24: {'sector':  4, 'time': (1405012239,1405012307)},
    25: {'sector':  4, 'time': (1405012323,1405012390)},

    26: {'sector':  5, 'time': (1405012398,1405012487)},
    27: {'sector':  5, 'time': (1405012499,1405012569)},
    31: {'sector':  5, 'time': (1405012863,1405012945)},
    32: {'sector':  5, 'time': (1405012959,1405013029)},
    33: {'sector':  5, 'time': (1405013045,1405013117)},

    28: {'sector':  6, 'time': (1405012576,1405012650)},
    29: {'sector':  6, 'time': (1405012660,1405012729)},
    30: {'sector':  6, 'time': (1405012771,1405012845)},
    34: {'sector':  6, 'time': (1405013121,1405013196)},
    35: {'sector':  6, 'time': (1405013283,1405013415)},

    16: {'sector':  7, 'time': (1405011434,1405011527)},
    17: {'sector':  7, 'time': (1405011536,1405011642)},
    21: {'sector':  7, 'time': (1405011931,1405011996)},
    22: {'sector':  7, 'time': (1405012020,1405012101)},
    23: {'sector':  7, 'time': (1405012151,1405012226)},

    59: {'sector':  8, 'time': (1405104149,1405104218)},
    60: {'sector':  8, 'time': (1405104227,1405104293)},
    64: {'sector':  8, 'time': (1405104547,1405104615)},
    65: {'sector':  8, 'time': (1405104623,1405104691)},
    66: {'sector':  8, 'time': (1405104699,1405104768)},

    51: {'sector':  9, 'time': (1405103524,1405103591)},
    52: {'sector':  9, 'time': (1405103604,1405103673)},
    53: {'sector':  9, 'time': (1405103684,1405103752)},
    57: {'sector':  9, 'time': (1405103997,1405104065)},
    58: {'sector':  9, 'time': (1405104075,1405104143)},

    49: {'sector': 10, 'time': (1405102287,1405102377)},
    50: {'sector': 10, 'time': (1405102978,1405103047)},
    54: {'sector': 10, 'time': (1405103762,1405103828)},
    55: {'sector': 10, 'time': (1405103845,1405103912)},
    56: {'sector': 10, 'time': (1405103923,1405103990)},

    61: {'sector': 11, 'time': (1405104301,1405104369)},
    62: {'sector': 11, 'time': (1405104380,1405104453)},
    63: {'sector': 11, 'time': (1405104466,1405104537)},
    67: {'sector': 11, 'time': (1405104774,1405104841)},
    68: {'sector': 11, 'time': (1405104856,1405104915)},

    36: {'sector': 12, 'time': (1405013435,1405013506)},
    37: {'sector': 12, 'time': (1405013527,1405013593)},
    38: {'sector': 12, 'time': (1405013605,1405013691)},
    39: {'sector': 12, 'time': (1405013781,1405013845)},
    40: {'sector': 12, 'time': (1405013857,1405013940)},
    41: {'sector': 12, 'time': (1405013951,1405014015)},
    42: {'sector': 12, 'time': (1405014022,1405014087)},
    43: {'sector': 12, 'time': (1405014107,1405014167)},
    44: {'sector': 12, 'time': (1405014172,1405014243)},
    45: {'sector': 12, 'time': (1405014299,1405014358)},
    46: {'sector': 12, 'time': (1405014367,1405014448)},
    47: {'sector': 12, 'time': (1405014455,1405014535)},
    48: {'sector': 12, 'time': (1405014543,1405014611)},

    101: {'sector':  0, 'time': (1405104952,1405105018)},
    102: {'sector':  0, 'time': (1405105025,1405105096)},
    103: {'sector':  0, 'time': (1405105102,1405105163)},
    104: {'sector':  0, 'time': (1405105169,1405105235)},
    105: {'sector':  0, 'time': (1405105241,1405105307)},
    106: {'sector':  0, 'time': (1405105312,1405105378)},
    107: {'sector':  0, 'time': (1405105385,1405105450)},
    108: {'sector':  0, 'time': (1405105457,1405105523)},
    109: {'sector':  0, 'time': (1405105530,1405105597)},
    110: {'sector':  0, 'time': (1405105602,1405105665)},
    111: {'sector':  0, 'time': (1405105671,1405105737)},
    112: {'sector':  0, 'time': (1405105744,1405105810)},
    113: {'sector':  0, 'time': (1405105818,1405105884)},
    114: {'sector':  0, 'time': (1405105891,1405105957)},
    115: {'sector':  0, 'time': (1405105963,1405106030)},
    116: {'sector':  0, 'time': (1405106050,1405106116)},
    117: {'sector':  0, 'time': (1405106132,1405106198)},
    118: {'sector':  0, 'time': (1405106205,1405106273)},
    119: {'sector':  0, 'time': (1405106280,1405106347)},
    120: {'sector':  0, 'time': (1405106354,1405106420)},
    121: {'sector':  0, 'time': (1405106426,1405106495)},
    122: {'sector':  0, 'time': (1405106504,1405106570)},
    199: {'sector':  0, 'time': (1405106603,1405106723)},
}