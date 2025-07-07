-- 1. ユーザーテーブル
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    mail_address VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    user_role VARCHAR(20) DEFAULT 'member', -- 例: 'admin', 'member'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 同好会イベントテーブル
CREATE TABLE clubs (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 参加者テーブル（多対多）
CREATE TABLE participants (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    club_id INTEGER NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, club_id)
);

-- 4. リンク管理テーブル（イベント単位で1つのリンク）
CREATE TABLE links (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    club_id INTEGER NOT NULL UNIQUE REFERENCES clubs(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
