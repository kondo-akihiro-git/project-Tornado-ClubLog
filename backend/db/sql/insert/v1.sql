-- ユーザーデータ（10件）
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
  ('emi', 'emi@example.com', 'hashed_pw10', 'member');

-- クラブデータ（10件）
INSERT INTO clubs (event_name)
VALUES
  ('ボードゲーム同好会'),
  ('ランニングサークル'),
  ('読書会'),
  ('映画鑑賞部'),
  ('英会話クラブ'),
  ('料理研究会'),
  ('写真散歩クラブ'),
  ('プログラミング勉強会'),
  ('カラオケ部'),
  ('ビジネス書討論会');

-- 参加者データ（多対多）計20件程度
INSERT INTO participants (user_id, club_id)
VALUES
  (1, 1), -- taro → ボードゲーム
  (2, 1), -- hanako → ボードゲーム
  (3, 1), -- jiro → ボードゲーム
  (1, 2), -- taro → ランニング
  (4, 2), -- yuki → ランニング
  (5, 3), -- aya → 読書会
  (6, 4), -- ken → 映画
  (7, 5), -- mika → 英会話
  (8, 6), -- sota → 料理
  (1, 6), -- taro → 料理
  (9, 7), -- kenta → 写真
  (10, 8), -- emi → プログラミング
  (3, 8), -- jiro → プログラミング
  (4, 9), -- yuki → カラオケ
  (5, 9), -- aya → カラオケ
  (6, 10), -- ken → ビジネス書
  (7, 10), -- mika → ビジネス書
  (8, 10), -- sota → ビジネス書
  (9, 3), -- kenta → 読書会
  (2, 7);  -- hanako → 写真散歩

-- リンクデータ（クラブごとに1件ずつ、計10件）
INSERT INTO links (url, club_id)
VALUES
  ('https://example.com/boardgame', 1),
  ('https://example.com/running', 2),
  ('https://example.com/bookclub', 3),
  ('https://example.com/movies', 4),
  ('https://example.com/english', 5),
  ('https://example.com/cooking', 6),
  ('https://example.com/photowalk', 7),
  ('https://example.com/devstudy', 8),
  ('https://example.com/karaoke', 9),
  ('https://example.com/businessbooks', 10);
