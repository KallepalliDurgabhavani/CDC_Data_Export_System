DO $$
BEGIN
  IF (SELECT COUNT(*) FROM users) = 0 THEN
    INSERT INTO users (name, email, created_at, updated_at, is_deleted)
    SELECT
      'User ' || g,
      'user' || g || '@example.com',
      NOW() - (random() * INTERVAL '30 days'),
      NOW() - (random() * INTERVAL '10 days'),
      random() < 0.01
    FROM generate_series(1, 100000) g;
  END IF;
END $$;