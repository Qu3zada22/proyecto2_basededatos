-- Insertar un evento
INSERT INTO evento (nombre, fecha) VALUES ('Concierto UVG 2025', '2025-05-20 18:00:00');

-- Insertar 100 asientos para el evento (id=1)
INSERT INTO asiento (evento_id, numero)
SELECT 1, generate_series(1, 100);

-- Reservar algunos asientos iniciales (en este caso 10 reservas)
INSERT INTO reserva (usuario_id, asiento_id)
SELECT floor(random() * 1000 + 1), id 
FROM asiento 
WHERE numero IN (1, 5, 10, 15, 20, 25, 30, 35, 40, 45);