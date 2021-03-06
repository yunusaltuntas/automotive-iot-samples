import sqlite3

from flask import current_app, g

def get_db():
    """
    Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            '../data/cloud_db.db',
            detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
        initialize_DB(g.db)
    return g.db

def initialize_DB(db):
    """
    Creating event table if it doesn't already exist.

    The event table has two keys:
    1-A key generated on the edge gateway when an event detected.
    2-The sqlite3 rowid: http://www.sqlitetutorial.net/sqlite-autoincrement/
    """
    db.execute( """CREATE TABLE IF NOT EXISTS events (client_side_id TEXT, user TEXT, event_type TEXT, event_timestamp INTEGER, gps_coord TEXT);""")

def write_event(json_data):
    """
    Inserts data passed in argument.
    """
    db = get_db()

    row_to_insert = [
        json_data["client_side_id"],
        json_data["user"],
        json_data["event_type"],
        int(json_data["event_timestamp"]),
        json_data["gps_coord"]
        ]

    db.execute("""INSERT OR REPLACE INTO events VALUES(?,?,?,?,?)""",row_to_insert)
    db.commit()

def read_last_event():
    """
    Reads last event from DB.
    """
    db = get_db()

    row = db.execute("""SELECT client_side_id, user, event_type, max(event_timestamp), gps_coord FROM events""").fetchall()

    return row

def read_events():
    """
    Reads last event from DB.
    """
    db = get_db()

    # Returning all events from DB
    # TODO: pagination
    rows = db.execute("""SELECT client_side_id, user, event_type, event_timestamp, gps_coord FROM events""").fetchall()

    return rows