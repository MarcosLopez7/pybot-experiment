CREATE TABLE EspecialChannel (
    id INTEGER PRIMARY KEY,
    guild_id VARCHAR(30) NOT NULL,
    channel_id VARCHAR(30) NOT NULL,
    type VARCHAR(25) NOT NULL,
    name VARCHAR(35) NOT NULL
);

CREATE SEQUENCE test_id_seq OWNED BY EspecialChannel.id;
ALTER TABLE EspecialChannel ALTER COLUMN id SET DEFAULT nextval('test_id_seq');

UPDATE
	EspecialChannel
SET
	id = nextval('test_id_seq');