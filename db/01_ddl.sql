-- Tabla Evento
CREATE TABLE evento (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha TIMESTAMP NOT NULL
);

-- Tabla Asiento
CREATE TABLE asiento (
    id SERIAL PRIMARY KEY,
    evento_id INTEGER NOT NULL,
    numero INTEGER NOT NULL,
    estado VARCHAR(20) DEFAULT 'disponible',
    FOREIGN KEY (evento_id) REFERENCES evento(id),
    UNIQUE (evento_id, numero)
);

-- Tabla Reserva
CREATE TABLE reserva (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    asiento_id INTEGER NOT NULL,
    fecha_reserva TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (asiento_id) REFERENCES asiento(id)
);