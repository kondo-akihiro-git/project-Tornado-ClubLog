-- 1. ユーザーデータ（20件）
INSERT INTO users (id, username, mail_address, password, user_role)
VALUES 
  (1, '山田太郎', 'test_admin@example.com', 'test', 'admin'),
  (2, '佐藤花子', 'test_owner@example.com', 'test', 'owner'),
  (3, '鈴木次郎', 'test_member@example.com', 'test', 'member'),
  (4, '高橋雪乃', 'yuki@example.com', 'hashed_pw4', 'admin'),
  (5, '伊藤彩', 'aya@example.com', 'hashed_pw5', 'owner'),
  (6, '渡辺健', 'ken@example.com', 'hashed_pw6', 'member'),
  (7, '中村美香', 'mika@example.com', 'hashed_pw7', 'member'),
  (8, '小林颯太', 'sota@example.com', 'hashed_pw8', 'member'),
  (9, '加藤健太', 'kenta@example.com', 'hashed_pw9', 'owner'),
  (10, '斉藤恵美', 'emi@example.com', 'hashed_pw10', 'member'),
  (11, '山本春', 'haru@example.com', 'hashed_pw11', 'member'),
  (12, '井上直樹', 'nao@example.com', 'hashed_pw12', 'member'),
  (13, '松本良介', 'ryo@example.com', 'hashed_pw13', 'owner'),
  (14, '清水咲', 'saki@example.com', 'hashed_pw14', 'member'),
  (15, '林純一', 'jun@example.com', 'hashed_pw15', 'member'),
  (16, '森田健一', 'mori@example.com', 'hashed_pw16', 'member'),
  (17, '竹内葵', 'aoi@example.com', 'hashed_pw17', 'member'),
  (18, '石井陽菜', 'haruna@example.com', 'hashed_pw18', 'member'),
  (19, '上田大輔', 'daisuke@example.com', 'hashed_pw19', 'owner'),
  (20, '橋本美月', 'mizuki@example.com', 'hashed_pw20', 'member');

-- 2. クラブ（owner_idは必ずownerのユーザー）
INSERT INTO clubs (id, name, owner_id)
VALUES
  (1, 'ボードゲーム同好会', 2),
  (2, 'ランニングサークル', 5),
  (3, '読書クラブ', 9),
  (4, '写真部', 13),
  (5, '料理研究会', 19);

-- 3. イベント（各クラブが複数開催）
INSERT INTO events (id, club_id, title, scheduled_at)
VALUES
  (1, 1, 'カタン大会', '2025-08-01 19:00:00'),
  (2, 1, 'ドミニオントーナメント', '2025-08-15 18:30:00'),
  (3, 2, '朝ラン@代々木公園', '2025-08-05 07:00:00'),
  (4, 2, 'ナイトラン@皇居', '2025-08-20 20:00:00'),
  (5, 3, '読書感想会#1', '2025-08-10 10:00:00'),
  (6, 3, '読書感想会#2', '2025-08-24 10:00:00'),
  (7, 4, '撮影遠足in鎌倉', '2025-08-12 09:00:00'),
  (8, 4, 'ポートレート練習会', '2025-08-28 14:00:00'),
  (9, 5, '夏野菜カレーを作る会', '2025-08-06 11:00:00'),
  (10, 5, '中華料理基礎講座', '2025-08-18 11:00:00'),
  (11, 1, 'UNOナイト', '2025-08-30 19:30:00'),
  (12, 2, 'トレイルラン体験会', '2025-08-22 06:00:00'),
  (13, 3, '名作読破会', '2025-08-31 13:00:00'),
  (14, 4, 'インスタ映え写真撮影会', '2025-08-25 15:00:00'),
  (15, 5, '韓国料理チャレンジ', '2025-08-14 12:00:00');

-- 4. 参加者（pending / approved / rejected をバランスよく）
INSERT INTO participants (user_id, event_id, approved_status)
VALUES
  (1, 1, 'pending'), (2, 1, 'approved'), (3, 1, 'rejected'),
  (4, 2, 'approved'), (5, 2, 'pending'), (6, 2, 'rejected'),
  (7, 3, 'approved'), (8, 3, 'pending'), (9, 3, 'rejected'),
  (10, 4, 'pending'), (11, 4, 'approved'), (12, 4, 'rejected'),
  (13, 5, 'pending'), (14, 5, 'approved'), (15, 5, 'rejected'),
  (16, 6, 'approved'), (17, 6, 'pending'), (18, 6, 'rejected'),
  (19, 7, 'pending'), (20, 7, 'approved'), (1, 7, 'rejected'),
  (2, 8, 'approved'), (3, 8, 'pending'), (4, 8, 'rejected'),
  (5, 9, 'pending'), (6, 9, 'approved'), (7, 9, 'rejected'),
  (8,10, 'approved'), (9,10, 'pending'), (10,10, 'rejected'),
  (11,11, 'pending'), (12,12, 'approved'), (13,13, 'rejected'),
  (14,14, 'approved'), (15,15, 'pending'), (16,15, 'rejected');

-- 5. リンク（イベントごと）
INSERT INTO links (url_token, event_id)
VALUES
  ('https://example.com/katan', 1),
  ('https://example.com/dominion', 2),
  ('https://example.com/yoyogi-run', 3),
  ('https://example.com/kokyo-run', 4),
  ('https://example.com/book1', 5),
  ('https://example.com/book2', 6),
  ('https://example.com/kamakura', 7),
  ('https://example.com/portrait', 8),
  ('https://example.com/curry', 9),
  ('https://example.com/chinese-cooking', 10),
  ('https://example.com/uno-night', 11),
  ('https://example.com/trail-run', 12),
  ('https://example.com/classic-book', 13),
  ('https://example.com/photo-spot', 14),
  ('https://example.com/korean-cooking', 15);
