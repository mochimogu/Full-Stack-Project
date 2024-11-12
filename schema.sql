CREATE TABLE CRUD (
    CRUD_ID PRIMARY KEY SERIAL,
    CONTENT VARCHAR(256),
    LAST_EDIT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CREATED DATE DEFAULT CURRENT_DATE
)