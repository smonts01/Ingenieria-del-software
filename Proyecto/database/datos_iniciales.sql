USE Stayfit_database;

-- Tarifas
INSERT IGNORE INTO tarifa (nombre, precio_mensual, servicios_incluidos, fecha_inicio) VALUES
('Basico',   30.00, 'Acceso a instalaciones y clases grupales', '2026-01-01'),
('Premium',  45.00, 'Acceso ilimitado, clases y entrenador personal', '2026-01-01');

-- Sala (necesaria para las clases)
INSERT IGNORE INTO sala (nombre, aforo_maximo, tipo_zona) VALUES
('Sala Principal', 20, 'colectiva');

-- Clases (usando el entrenador con id_usuario=2, admin con id_usuario=1)
-- Ajusta id_entrenador y id_administrador_registra según tus datos
INSERT IGNORE INTO clase (id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad) VALUES
(2, 1, 'Spinning',  450, 'lunes',    '09:00', '10:00', 60, 20, 'alta'),
(2, 1, 'Zumba',     350, 'martes',   '10:00', '11:00', 60, 20, 'media'),
(2, 1, 'Yoga',      200, 'miercoles','09:00', '10:00', 60, 20, 'baja'),
(2, 1, 'Pilates',   250, 'jueves',   '10:00', '11:00', 60, 20, 'baja'),
(2, 1, 'Crossfit',  600, 'viernes',  '09:00', '10:00', 60, 20, 'alta');
