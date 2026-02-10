CREATE TABLE IF NOT EXISTS tokens(
    id SERIAL PRIMARY KEY,
    access_token VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tokens_created_at ON token(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_tokens_expires_at ON token(expires_at);