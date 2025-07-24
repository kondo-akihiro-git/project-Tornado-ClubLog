-- 1. ユーザーデータ（15件）← id 明示
INSERT INTO users (id, username, mail_address, password, user_role)
VALUES 
  (1, 'taro', 'taro@example.com', 'test', 'admin'),
  (2, 'hanako', 'hanako@example.com', 'test', 'member'),
  (3, 'jiro', 'jiro@example.com', 'test', 'member'),
  (4, 'yuki', 'yuki@example.com', 'hashed_pw4', 'admin'),
  (5, 'aya', 'aya@example.com', 'hashed_pw5', 'member'),
  (6, 'ken', 'ken@example.com', 'hashed_pw6', 'member'),
  (7, 'mika', 'mika@example.com', 'hashed_pw7', 'member'),
  (8, 'sota', 'sota@example.com', 'hashed_pw8', 'member'),
  (9, 'kenta', 'kenta@example.com', 'hashed_pw9', 'admin'),
  (10, 'emi', 'emi@example.com', 'hashed_pw10', 'member'),
  (11, 'haru', 'haru@example.com', 'hashed_pw11', 'member'),
  (12, 'nao', 'nao@example.com', 'hashed_pw12', 'member'),
  (13, 'ryo', 'ryo@example.com', 'hashed_pw13', 'admin'),
  (14, 'saki', 'saki@example.com', 'hashed_pw14', 'member'),
  (15, 'jun', 'jun@example.com', 'hashed_pw15', 'member');

-- 2. クラブデータ（owner_idはusers.idと一致）
INSERT INTO clubs (id, name, owner_id)
VALUES
  (1, 'ボードゲーム同好会', 1),
  (2, 'ランニングサークル', 4),
  (3, '読書クラブ', 5),
  (4, '写真部', 9),
  (5, '料理研究会', 13);

-- 3. イベントデータ（各クラブが開催）
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

-- 4. 参加者データ（イベントごとの参加者）
INSERT INTO participants (user_id, event_id, approved_status)
VALUES
  (1, 1, 'pending'), (2, 1, 'pending'), (3, 1, 'pending'),
  (1, 2, 'pending'), (4, 2, 'pending'),
  (1, 3, 'pending'), (5, 3, 'pending'),
  (6, 4, 'pending'), (7, 4, 'pending'),
  (8, 5, 'pending'), (2, 5, 'pending'),
  (9, 6, 'pending'), (10, 6, 'pending'),
  (3, 7, 'pending'), (4, 7, 'pending'),
  (5, 8, 'pending'), (6, 8, 'pending'),
  (7, 9, 'pending'), (1, 9, 'pending'),
  (2,10, 'pending'), (3,10, 'pending'),
  (11,11, 'pending'), (12,12, 'pending'),
  (13,13, 'pending'), (14,14, 'pending'),
  (15,15, 'pending');


-- 5. リンクデータ（イベントごとに1リンク）
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
