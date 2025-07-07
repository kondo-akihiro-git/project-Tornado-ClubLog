-- ユーザーテーブル
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    mail_address VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    user_role VARCHAR(20) DEFAULT 'member', -- 例: 'admin', 'member'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 同好会（団体）テーブル
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- イベントテーブル（各同好会が開催するイベント）
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    club_id INTEGER NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    scheduled_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 参加者テーブル（イベントごとの参加者）
CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, event_id)
);

-- イベントごとのリンク
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    event_id INTEGER NOT NULL UNIQUE REFERENCES events(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



