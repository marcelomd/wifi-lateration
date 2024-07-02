# -*- coding: utf-8 -*-

import os

# From AWS
db_endpoint = os.environ.get('DB_ENDPOINT')
db_name = 'ebdb'
db_port = 3306
db_username = 'field7mysql'
db_password = 'field7mysql'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (db_username, db_password, db_endpoint, db_name)

# Keep DB small

db_flush_interval = 60
db_flush_limit = 1800

# Barra Shopping:
aps = [
    {"name": "24", "mac": 0xAC86741082A0, "lat": 0.0, "lng": 0.0},
    {"name": "19", "mac": 0xAC86741082A8, "lat": 0.0, "lng": 0.0},
    {"name": "12", "mac": 0xAC86741082B0, "lat": 0.0, "lng": 0.0},
    {"name": "20", "mac": 0xAC86741082B8, "lat": 0.0, "lng": 0.0},
    {"name": "23", "mac": 0xAC86741082C0, "lat": 0.0, "lng": 0.0},
    {"name": "22", "mac": 0xAC86741082C8, "lat": 0.0, "lng": 0.0},
    #{"name": "GVT2", "mac": 0xAC86741082D0, "lat": 0.0, "lng": 0.0}, # Gateway
    {"name": "17", "mac": 0xAC86741082D8, "lat": 0.0, "lng": 0.0},
    #{"name": "RACK11", "mac": 0xAC86741082E0, "lat": 0.0, "lng": 0.0}, # Gateway
    {"name": "18", "mac": 0xAC86741082E8, "lat": 0.0, "lng": 0.0},
    {"name": "25", "mac": 0xAC86741082F0, "lat": 0.0, "lng": 0.0},
    {"name": "26", "mac": 0xAC8674108308, "lat": 0.0, "lng": 0.0},
    #{"name": "GVT1", "mac": 0xAC8674108310, "lat": 0.0, "lng": 0.0}, # Gateway
    {"name": "10", "mac": 0xAC8674108318, "lat": 0.0, "lng": 0.0},
    {"name": "16", "mac": 0xAC8674108320, "lat": 0.0, "lng": 0.0},
    {"name": "28", "mac": 0xAC8674108328, "lat": 0.0, "lng": 0.0},
    {"name": "27", "mac": 0xAC8674108330, "lat": 0.0, "lng": 0.0},
    {"name": "21", "mac": 0xAC8674108338, "lat": 0.0, "lng": 0.0},
    {"name": "4", "mac": 0xAC867410BE00, "lat": 0.0, "lng": 0.0},
    {"name": "6", "mac": 0xAC867410BE08, "lat": 0.0, "lng": 0.0},
    {"name": "8", "mac": 0xAC867410BE10, "lat": 0.0, "lng": 0.0},
    {"name": "9", "mac": 0xAC867410BE18, "lat": 0.0, "lng": 0.0},
    {"name": "7", "mac": 0xAC867410BE20, "lat": 0.0, "lng": 0.0},
    {"name": "11", "mac": 0xAC867410BE28, "lat": 0.0, "lng": 0.0},
    {"name": "1", "mac": 0xAC867410BE30, "lat": 0.0, "lng": 0.0},
    {"name": "14", "mac": 0xAC867410BE38, "lat": 0.0, "lng": 0.0},
    {"name": "13", "mac": 0xAC867410BE40, "lat": 0.0, "lng": 0.0},
    {"name": "15", "mac": 0xAC867410BE48, "lat": 0.0, "lng": 0.0},
    {"name": "5", "mac": 0xAC867410EA10, "lat": 0.0, "lng": 0.0},
    {"name": "3", "mac": 0xAC867410EA18, "lat": 0.0, "lng": 0.0},
    {"name": "2", "mac": 0xAC867410EA30, "lat": 0.0, "lng": 0.0},
]
