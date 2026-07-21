CREATE TYPE page AS ENUM ('county', 'duchy', 'kingdom', 'empire', 'hegemony');
CREATE TABLE log (
    id SERIAL PRIMARY KEY,
    page_name page NOT NULL,
    last_checked TIMESTAMPTZ NOT NULL,
    last_update TIMESTAMPTZ NOT NULL,
    status VARCHAR(50) NOT NULL
);

INSERT INTO log (page_name, last_checked, last_update, status)
VALUES
    ('county', '2025-07-21 23:00:00', '2024-04-21 23:00:00', 'not-changed'),
    ('duchy', '2025-07-21 23:00:00', '2024-04-21 23:00:00', 'not-changed'),
    ('kingdom', '2025-07-21 23:00:00', '2024-04-21 23:00:00', 'not-changed'),
    ('empire', '2025-07-21 23:00:00', '2024-04-21 23:00:00', 'not-changed'),
    ('hegemony', '2025-07-21 23:00:00', '2024-04-21 23:00:00', 'not-changed');