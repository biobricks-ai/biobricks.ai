CREATE TABLE user_event(
 user_event_id Integer PRIMARY KEY,
 create_time DATE DEFAULT (datetime('now','localtime')),
 uid   INTEGER NOT NULL,
 event TEXT NOT NULL,
 jsval TEXT NOT NULL  
)