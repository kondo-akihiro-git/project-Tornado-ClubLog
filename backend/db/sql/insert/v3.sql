-- ユーザーデータ（15件）
INSERT INTO users (username, mail_address, password, user_role)
VALUES 
  ('taro', 'taro@example.com', 'hashed_pw1', 'admin'),
  ('hanako', 'hanako@example.com', 'hashed_pw2', 'member'),
  ('jiro', 'jiro@example.com', 'hashed_pw3', 'member'),
  ('yuki', 'yuki@example.com', 'hashed_pw4', 'admin'),
  ('aya', 'aya@example.com', 'hashed_pw5', 'member'),
  ('ken', 'ken@example.com', 'hashed_pw6', 'member'),
  ('mika', 'mika@example.com', 'hashed_pw7', 'member'),
  ('sota', 'sota@example.com', 'hashed_pw8', 'member'),
  ('kenta', 'kenta@example.com', 'hashed_pw9', 'admin'),
  ('emi', 'emi@example.com', 'hashed_pw10', 'member'),
  ('haru', 'haru@example.com', 'hashed_pw11', 'member'),
  ('nao', 'nao@example.com', 'hashed_pw12', 'member'),
  ('ryo', 'ryo@example.com', 'hashed_pw13', 'admin'),
  ('saki', 'saki@example.com', 'hashed_pw14', 'member'),
  ('jun', 'jun@example.com', 'hashed_pw15', 'member');

-- クラブデータ（5件、owner_id = users.id）
INSERT INTO clubs (name, owner_id)
VALUES
  ('ボードゲーム同好会', 1),
  ('ランニングサークル', 4),
  ('読書クラブ', 5),
  ('写真部', 9),
  ('料理研究会', 13);

-- イベントデータ（各クラブが開催したイベント15件）
INSERT INTO events (club_id, title, scheduled_at)
VALUES
  (1, 'カタン大会', '2025-08-01 19:00:00'),
  (1, 'ドミニオントーナメント', '2025-08-15 18:30:00'),
  (2, '朝ラン@代々木公園', '2025-08-05 07:00:00'),
  (2, 'ナイトラン@皇居', '2025-08-20 20:00:00'),
  (3, '読書感想会#1', '2025-08-10 10:00:00'),
  (3, '読書感想会#2', '2025-08-24 10:00:00'),
  (4, '撮影遠足in鎌倉', '2025-08-12 09:00:00'),
  (4, 'ポートレート練習会', '2025-08-28 14:00:00'),
  (5, '夏野菜カレーを作る会', '2025-08-06 11:00:00'),
  (5, '中華料理基礎講座', '2025-08-18 11:00:00'),
  (1, 'UNOナイト', '2025-08-30 19:30:00'),
  (2, 'トレイルラン体験会', '2025-08-22 06:00:00'),
  (3, '名作読破会', '2025-08-31 13:00:00'),
  (4, 'インスタ映え写真撮影会', '2025-08-25 15:00:00'),
  (5, '韓国料理チャレンジ', '2025-08-14 12:00:00');

-- 参加者データ（イベントごとの参加者 20件以上）
INSERT INTO participants (user_id, event_id)
VALUES
  (1, 1), (2, 1), (3, 1),
  (1, 2), (4, 2),
  (1, 3), (5, 3),
  (6, 4), (7, 4),
  (8, 5), (2, 5),
  (9, 6), (10, 6),
  (3, 7), (4, 7),
  (5, 8), (6, 8),
  (7, 9), (1, 9),
  (2,10), (3,10),
  (11,11), (12,12),
  (13,13), (14,14),
  (15,15);

-- リンクデータ（イベントごとに1リンク）
INSERT INTO links (url, event_id)
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
