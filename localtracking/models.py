# -*- coding: utf-8 -*-

from database import db
from time import time


class AP(db.Model):
    """Access Point."""

    __tablename__ = "aps"
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(32))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, mac=0, name="default", lat=0.0, lng=0.0):
        self.mac = mac
        self.name = name
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return "(AP %012x : %s)" % (self.mac, self.name)


class Device(db.Model):
    """Device seen by access point."""

    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.BigInteger, unique=True)

    def __init__(self, mac=0):
        self.mac = mac

    def __repr__(self):
        return "(Device: %012x)" % self.mac


class NodeReport(db.Model):
    """Report sent by an access point."""

    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    t = db.Column(db.Integer)
    rss = db.Column(db.Integer)
    count = db.Column(db.Integer)
    ap_id = db.Column(db.Integer, db.ForeignKey("aps.id"))
    dev_id = db.Column(db.Integer, db.ForeignKey("devices.id"))
    ap = db.relationship("AP", backref="reports")
    dev = db.relationship("Device", backref="reports")

    def __init__(self, ap, dev, t, rss, count):
        self.t = t
        self.rss = rss
        self.count = count
        self.ap = ap
        self.dev = dev

    def __repr__(self):
        return "(%d: %012x <- (%d/%d) %012x | %d)" % (
            self.t,
            self.ap.mac,
            self.rss,
            self.count,
            self.dev.mac,
        )
