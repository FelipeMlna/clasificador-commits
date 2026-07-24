CREATE USER app_ia WITH PASSWORD 'clave_app_ia';

CREATE TABLE IF NOT EXISTS inferencias (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    motor VARCHAR(20) NOT NULL,
    resultado VARCHAR(20) NOT NULL,
    latencia_ms INTEGER,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT CONNECT ON DATABASE iadb TO app_ia;
GRANT USAGE ON SCHEMA public TO app_ia;
GRANT SELECT, INSERT ON TABLE inferencias TO app_ia;

GRANT USAGE, SELECT ON SEQUENCE inferencias_id_seq TO app_ia;
