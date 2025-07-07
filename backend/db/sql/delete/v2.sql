-- データ削除（依存関係の深いテーブルから順に）
DELETE FROM participants;
DELETE FROM links;
DELETE FROM events;
DELETE FROM clubs;
DELETE FROM users;

-- テーブル削除（依存関係を逆順で）
DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS users;
