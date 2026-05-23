USE Stayfit_database;

-- Eliminar clases con "matutino" en el nombre
DELETE FROM clase WHERE LOWER(nombre_actividad) LIKE '%matutino%';

-- Asegurarse de que solo existen estas 5 clases (sin matutino)
-- Si ya existen con el nombre exacto no hace nada (INSERT IGNORE)
INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
SELECT e.id_entrenador, 1, 'Spinning', 450, 'lunes', '09:00', '10:00', 60, 20, 'alta'
FROM entrenador e LIMIT 1;

INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
SELECT e.id_entrenador, 1, 'Zumba', 350, 'martes', '10:00', '11:00', 60, 20, 'media'
FROM entrenador e LIMIT 1;

INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
SELECT e.id_entrenador, 1, 'Yoga', 200, 'miercoles', '09:00', '10:00', 60, 20, 'baja'
FROM entrenador e LIMIT 1;

INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
SELECT e.id_entrenador, 1, 'Pilates', 250, 'jueves', '10:00', '11:00', 60, 20, 'baja'
FROM entrenador e LIMIT 1;

INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
SELECT e.id_entrenador, 1, 'Crossfit', 600, 'viernes', '09:00', '10:00', 60, 20, 'alta'
FROM entrenador e LIMIT 1;

-- Tarifas
INSERT IGNORE INTO tarifa (nombre, precio_mensual, servicios_incluidos, fecha_inicio)
VALUES ('Basico', 30.00, 'Acceso a instalaciones y clases grupales', '2026-01-01');

INSERT IGNORE INTO tarifa (nombre, precio_mensual, servicios_incluidos, fecha_inicio)
VALUES ('Premium', 45.00, 'Acceso ilimitado, clases y entrenador personal', '2026-01-01');

-- Ver clases resultantes
SELECT id_clase, nombre_actividad FROM clase;
