CREATE TABLE user (
 uid   INTEGER PRIMARY KEY,
 email TEXT NOT NULL UNIQUE,
 token TEXT NOT NULL UNIQUE,
 stripe_customer_id TEXT NOT NULL UNIQUE,
 hashpw TEXT NOT NULL,
 email_verified BOOL DEFAULT 0 CHECK (email_verified IN (0, 1))
);
