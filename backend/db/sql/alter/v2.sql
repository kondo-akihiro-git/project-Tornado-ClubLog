-- users テーブルの updated_at を JST に
ALTER TABLE users
ALTER COLUMN updated_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo');

-- clubs テーブルの created_at を JST に
ALTER TABLE clubs
ALTER COLUMN created_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo');

-- events テーブルの created_at を JST に
ALTER TABLE events
ALTER COLUMN created_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo');

-- participants テーブルの joined_at を JST に
ALTER TABLE participants
ALTER COLUMN joined_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo');

-- links テーブルの created_at を JST に
ALTER TABLE links
ALTER COLUMN created_at SET DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Tokyo');
