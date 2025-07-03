-- 依存関係を考慮して、下位テーブルから順に削除
DELETE FROM participants;
DELETE FROM links;
DELETE FROM clubs;
DELETE FROM users;

-- 外部キー依存のある順序に注意してDROP
DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS users;
