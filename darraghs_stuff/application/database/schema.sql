CREATE TABLE users (
    username TEXT NOT NULL UNIQUE,
    password CHAR(120) NOT NULL
);

INSERT INTO users VALUES (
    'admin',
    '243262243132246f6b3835716e6a55446e50304c51675833624962347561566a53646855676179725a61777937706f726d4b73466d6f715975687a75'
);