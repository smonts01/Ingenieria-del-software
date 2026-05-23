DROP DATABASE IF EXISTS Stayfit_database;
CREATE DATABASE Stayfit_database
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE Stayfit_database;

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT chk_roles_nombre CHECK (
        nombre_rol IN ('cliente', 'entrenador', 'recepcionista', 'administrador', 'contable')
    )
);

INSERT INTO roles (nombre_rol) VALUES
('cliente'),
('entrenador'),
('recepcionista'),
('administrador'),
('contable');

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(9) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_nacimiento DATE NOT NULL,

    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE registro_acceso (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_acceso VARCHAR(20) NOT NULL,

    CONSTRAINT chk_registro_tipo_acceso CHECK (tipo_acceso IN ('entrada', 'salida')),

    CONSTRAINT fk_registro_acceso_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    estado_pagado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    calorias_acumuladas INT NOT NULL DEFAULT 0,

    CONSTRAINT chk_cliente_estado_pagado CHECK (estado_pagado IN ('abonado', 'pendiente')),
    CONSTRAINT chk_cliente_calorias CHECK (calorias_acumuladas >= 0),

    CONSTRAINT fk_cliente_usuario
        FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    salario DECIMAL(10,2) NOT NULL,

    CONSTRAINT chk_empleado_salario CHECK (salario >= 0),

    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (id_empleado) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE menor (
    id_cliente INT PRIMARY KEY,
    dni_tutor VARCHAR(9) NOT NULL,
    nombre_tutor VARCHAR(100) NOT NULL,

    CONSTRAINT fk_menor_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE adulto (
    id_cliente INT PRIMARY KEY,

    CONSTRAINT fk_adulto_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE administrador (
    id_administrador INT PRIMARY KEY,

    CONSTRAINT fk_administrador_empleado
        FOREIGN KEY (id_administrador) REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE entrenador (
    id_entrenador INT PRIMARY KEY,
    especialidad VARCHAR(100) NOT NULL,
    id_administrador_registra INT NOT NULL,

    CONSTRAINT fk_entrenador_empleado
        FOREIGN KEY (id_entrenador) REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_entrenador_administrador
        FOREIGN KEY (id_administrador_registra) REFERENCES administrador(id_administrador)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE recepcionista (
    id_recepcionista INT PRIMARY KEY,
    turno VARCHAR(50) NOT NULL,
    id_administrador_registra INT NOT NULL,

    CONSTRAINT fk_recepcionista_empleado
        FOREIGN KEY (id_recepcionista) REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_recepcionista_administrador
        FOREIGN KEY (id_administrador_registra) REFERENCES administrador(id_administrador)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE contable (
    id_contable INT PRIMARY KEY,
    titulacion VARCHAR(100) NOT NULL,
    id_administrador_registra INT NOT NULL,

    CONSTRAINT fk_contable_empleado
        FOREIGN KEY (id_contable) REFERENCES empleados(id_empleado)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_contable_administrador
        FOREIGN KEY (id_administrador_registra) REFERENCES administrador(id_administrador)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    aforo_maximo INT NOT NULL,
    tipo_zona VARCHAR(50) NOT NULL,

    CONSTRAINT chk_sala_aforo CHECK (aforo_maximo > 0)
);

CREATE TABLE clase (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    id_entrenador INT NOT NULL,
    id_sala INT NOT NULL,
    nombre_actividad VARCHAR(80) NOT NULL,
    calorias_estimadas INT NOT NULL DEFAULT 0,
    dia_semana VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    duracion INT NOT NULL,
    aforo_maximo INT NOT NULL,
    nivel_intensidad VARCHAR(20) NOT NULL,

    CONSTRAINT chk_clase_nivel CHECK (nivel_intensidad IN ('baja', 'media', 'alta')),
    CONSTRAINT chk_clase_calorias CHECK (calorias_estimadas >= 0),
    CONSTRAINT chk_clase_duracion CHECK (duracion > 0),
    CONSTRAINT chk_clase_aforo CHECK (aforo_maximo > 0),
    CONSTRAINT chk_clase_horas CHECK (hora_fin > hora_inicio),

    CONSTRAINT fk_clase_entrenador
        FOREIGN KEY (id_entrenador) REFERENCES entrenador(id_entrenador)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT fk_clase_sala
        FOREIGN KEY (id_sala) REFERENCES sala(id_sala)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE asistencia (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_clase INT NOT NULL,
    fecha DATE NOT NULL,
    presente VARCHAR(5) NOT NULL,

    CONSTRAINT chk_asistencia_presente CHECK (presente IN ('si', 'no')),

    CONSTRAINT fk_asistencia_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_asistencia_clase
        FOREIGN KEY (id_clase) REFERENCES clase(id_clase)
        ON UPDATE RESTRICT
        ON DELETE CASCADE
);

CREATE TABLE inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_clase INT NOT NULL,
    fecha_inscripcion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'inscrito',

    CONSTRAINT chk_inscripcion_estado CHECK (estado IN ('inscrito', 'cancelado')),
    CONSTRAINT uq_cliente_clase UNIQUE (id_cliente, id_clase),

    CONSTRAINT fk_inscripcion_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_inscripcion_clase
        FOREIGN KEY (id_clase) REFERENCES clase(id_clase)
        ON UPDATE RESTRICT
        ON DELETE CASCADE
);

CREATE TABLE tarifa (
    id_tarifa INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    precio_mensual DECIMAL(10,2) NOT NULL,
    servicios_incluidos TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NULL,

    CONSTRAINT chk_tarifa_precio CHECK (precio_mensual > 0),
    CONSTRAINT chk_tarifa_fechas CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
);

CREATE TABLE cliente_tarifa (
    id_cliente_tarifa INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_tarifa INT NOT NULL,
    fecha_contratacion DATE NOT NULL DEFAULT (CURRENT_DATE),
    estado VARCHAR(20) NOT NULL DEFAULT 'activa',

    CONSTRAINT chk_cliente_tarifa_estado CHECK (estado IN ('activa', 'caducada', 'cancelada')),

    CONSTRAINT fk_cliente_tarifa_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_cliente_tarifa_tarifa
        FOREIGN KEY (id_tarifa) REFERENCES tarifa(id_tarifa)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_contable INT NOT NULL,
    id_tarifa INT NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(30) NOT NULL,
    fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    tipo_cuota VARCHAR(50) NOT NULL,

    CONSTRAINT chk_pago_metodo CHECK (metodo_pago IN ('efectivo', 'tarjeta', 'transferencia', 'bizum')),
    CONSTRAINT chk_pago_estado CHECK (estado IN ('abonado', 'pendiente')),
    CONSTRAINT chk_pago_importe CHECK (importe > 0),

    CONSTRAINT fk_pago_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_pago_contable
        FOREIGN KEY (id_contable) REFERENCES contable(id_contable)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT fk_pago_tarifa
        FOREIGN KEY (id_tarifa) REFERENCES tarifa(id_tarifa)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE informe (
    id_informe INT AUTO_INCREMENT PRIMARY KEY,
    id_contable INT NOT NULL,
    tipo_informe VARCHAR(80) NOT NULL,
    fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_informe_contable
        FOREIGN KEY (id_contable) REFERENCES contable(id_contable)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

DELIMITER //

CREATE TRIGGER trg_clasificar_cliente
AFTER INSERT ON clientes
FOR EACH ROW
BEGIN
    DECLARE edad INT;

    SELECT TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE())
    INTO edad
    FROM usuarios
    WHERE id_usuario = NEW.id_cliente;

    IF edad < 18 THEN
        INSERT INTO menor (id_cliente, dni_tutor, nombre_tutor)
        VALUES (NEW.id_cliente, 'PENDIENTE', 'PENDIENTE');
    ELSE
        INSERT INTO adulto (id_cliente)
        VALUES (NEW.id_cliente);
    END IF;
END//

DELIMITER ;



INSERT INTO usuarios
(id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento)
VALUES
(1, '00000001A', 'Admin Principal', '600000001', 'admin@stayfit.com', 'admin', 'admin1', 4, 'Calle Admin 1', '1980-01-01'),
(2, '00000002B', 'Carlos Entrenador', '600000002', 'carlos@stayfit.com', 'entrenador', 'entrenador1', 2, 'Calle Entrenador 2', '1990-02-02'),
(10, '11111111A', 'Marta González', '600111111', 'marta@stayfit.com', 'marta', 'marta1', 1, 'Calle Uno', '2000-05-10'),
(11, '22222222B', 'Pablo Ruiz', '600222222', 'pablo@stayfit.com', 'pablo', 'pablo1', 1, 'Calle Dos', '1998-03-15'),
(12, '33333333C', 'Lucía Pérez', '600333333', 'lucia@stayfit.com', 'lucia', 'lucia1', 1, 'Calle Tres', '2001-07-20');

INSERT INTO empleados (id_empleado, salario) VALUES
(1, 2000.00),
(2, 1600.00);

INSERT INTO administrador (id_administrador) VALUES
(1);

INSERT INTO entrenador (id_entrenador, especialidad, id_administrador_registra) VALUES
(2, 'Fitness y clases dirigidas', 1);

INSERT INTO clientes (id_cliente, estado_pagado, calorias_acumuladas) VALUES
(10, 'abonado', 0),
(11, 'abonado', 0),
(12, 'pendiente', 0);

INSERT INTO sala (id_sala, nombre, aforo_maximo, tipo_zona) VALUES
(1, 'Sala Agility', 25, 'Agility'),
(2, 'Zona Speed', 19, 'Speed'),
(3, 'Zona Cross', 12, 'Cross');

INSERT INTO clase
(id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
VALUES
(1, 2, 1, 'Yoga Matutino', 250, 'lunes', '09:00:00', '10:00:00', 60, 25, 'media'),
(2, 2, 2, 'Spinning Intenso', 500, 'miércoles', '18:00:00', '19:00:00', 60, 19, 'alta'),
(3, 2, 1, 'Pilates', 300, 'viernes', '11:00:00', '12:00:00', 60, 25, 'media');

INSERT INTO inscripcion (id_cliente, id_clase, estado) VALUES
(10, 1, 'inscrito'),
(11, 1, 'inscrito'),
(12, 1, 'inscrito'),
(10, 2, 'inscrito'),
(11, 3, 'inscrito');