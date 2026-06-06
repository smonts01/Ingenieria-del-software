DROP DATABASE IF EXISTS stayfit_database;

CREATE DATABASE stayfit_database
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE stayfit_database;

-- =====================================================
-- ROLES
-- =====================================================

CREATE TABLE roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(30) NOT NULL UNIQUE,
    CONSTRAINT chk_roles_nombre CHECK (
        nombre_rol IN ('cliente', 'entrenador', 'recepcionista', 'administrador', 'contable')
    )
);

-- =====================================================
-- SALARIOS FIJOS POR TIPO DE TRABAJADOR
-- =====================================================

CREATE TABLE salario_trabajador (
    id_salario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol INT NOT NULL UNIQUE,
    nombre_puesto VARCHAR(50) NOT NULL UNIQUE,
    salario_base DECIMAL(10,2) NOT NULL,

    CONSTRAINT chk_salario_base CHECK (
        salario_base >= 0
    ),

    CONSTRAINT fk_salario_trabajador_rol
        FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =====================================================
-- USUARIOS
-- =====================================================

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

-- =====================================================
-- REGISTRO DE ACCESO
-- =====================================================

CREATE TABLE registro_acceso (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_hora_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_acceso VARCHAR(20) NOT NULL,

    CONSTRAINT chk_registro_tipo_acceso CHECK (
        tipo_acceso IN ('entrada', 'salida')
    ),

    CONSTRAINT fk_registro_acceso_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- =====================================================
-- CLIENTES
-- =====================================================

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    estado_pagado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    calorias_acumuladas INT NOT NULL DEFAULT 0,

    CONSTRAINT chk_cliente_estado_pagado CHECK (
        estado_pagado IN ('abonado', 'pendiente')
    ),

    CONSTRAINT chk_cliente_calorias CHECK (
        calorias_acumuladas >= 0
    ),

    CONSTRAINT fk_cliente_usuario
        FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario)
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

-- =====================================================
-- EMPLEADOS
-- =====================================================

CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    salario DECIMAL(10,2) NOT NULL,

    CONSTRAINT chk_empleado_salario CHECK (
        salario >= 0
    ),

    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (id_empleado) REFERENCES usuarios(id_usuario)
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

-- =====================================================
-- SALAS Y CLASES
-- =====================================================

CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    aforo_maximo INT NOT NULL,

    CONSTRAINT chk_sala_aforo CHECK (
        aforo_maximo > 0
    )
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

    CONSTRAINT chk_clase_nivel CHECK (
        nivel_intensidad IN ('baja', 'media', 'alta')
    ),

    CONSTRAINT chk_clase_calorias CHECK (
        calorias_estimadas >= 0
    ),

    CONSTRAINT chk_clase_duracion CHECK (
        duracion > 0
    ),

    CONSTRAINT chk_clase_aforo CHECK (
        aforo_maximo > 0
    ),

    CONSTRAINT chk_clase_horas CHECK (
        hora_fin > hora_inicio
    ),

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

    CONSTRAINT chk_asistencia_presente CHECK (
        presente IN ('si', 'no')
    ),

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

    CONSTRAINT chk_inscripcion_estado CHECK (
        estado IN ('inscrito', 'cancelado')
    ),

    CONSTRAINT uq_cliente_clase UNIQUE (
        id_cliente, id_clase
    ),

    CONSTRAINT fk_inscripcion_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_inscripcion_clase
        FOREIGN KEY (id_clase) REFERENCES clase(id_clase)
        ON UPDATE RESTRICT
        ON DELETE CASCADE
);

-- =====================================================
-- TARIFAS Y PAGOS
-- =====================================================

CREATE TABLE tarifa (
    id_tarifa INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    precio_mensual DECIMAL(10,2) NOT NULL,
    servicios_incluidos TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,

    CONSTRAINT chk_tarifa_precio CHECK (
        precio_mensual > 0
    )
);

CREATE TABLE cliente_tarifa (
    id_cliente_tarifa INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_tarifa INT NOT NULL,
    fecha_contratacion DATE NOT NULL DEFAULT (CURRENT_DATE),
    estado VARCHAR(20) NOT NULL DEFAULT 'activa',

    CONSTRAINT chk_cliente_tarifa_estado CHECK (
        estado IN ('activa', 'cancelada')
    ),

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

    CONSTRAINT chk_pago_metodo CHECK (
        metodo_pago IN ('efectivo', 'tarjeta', 'transferencia', 'bizum')
    ),

    CONSTRAINT chk_pago_importe CHECK (
        importe > 0
    ),

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

-- =====================================================
-- DATOS INICIALES
-- =====================================================

INSERT INTO roles (id_rol, nombre_rol)
VALUES
(1, 'cliente'),
(2, 'entrenador'),
(3, 'recepcionista'),
(4, 'administrador'),
(5, 'contable');

INSERT INTO salario_trabajador
(id_rol, nombre_puesto, salario_base)
VALUES
(2, 'entrenador', 1600.00),
(3, 'recepcionista', 1200.00),
(4, 'administrador', 2000.00),
(5, 'contable', 1800.00);

-- =====================================================
-- ADMINISTRADOR INICIAL
-- Usuario: admin
-- Contraseña: admin1
-- =====================================================

INSERT INTO usuarios
(id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento)
VALUES
(1, '00000001A', 'Admin Principal', '600000001', 'admin@stayfit.com', 'admin', 'admin1', 4, 'Calle Admin 1', '1980-01-01');

INSERT INTO empleados
(id_empleado, salario)
SELECT 
    1,
    salario_base
FROM salario_trabajador
WHERE nombre_puesto = 'administrador';

INSERT INTO administrador
(id_administrador)
VALUES
(1);

-- =====================================================
-- ENTRENADOR FIJO PARA LAS CLASES
-- Usuario: entrenador
-- Contraseña: entrenador1
-- =====================================================

INSERT INTO usuarios
(id_usuario, dni, nombre, telefono, email, username, password_hash, id_rol, direccion, fecha_nacimiento)
VALUES
(2, '00000002B', 'Entrenador Principal', '600000002', 'entrenador@stayfit.com', 'entrenador', 'entrenador1', 2, 'Calle Entrenador 1', '1990-02-02');

INSERT INTO empleados
(id_empleado, salario)
SELECT 
    2,
    salario_base
FROM salario_trabajador
WHERE nombre_puesto = 'entrenador';

INSERT INTO entrenador
(id_entrenador, id_administrador_registra)
VALUES
(2, 1);

-- =====================================================
-- TARIFAS FIJAS
-- =====================================================

INSERT INTO tarifa
(id_tarifa, nombre, precio_mensual, servicios_incluidos, fecha_inicio)
VALUES
(1, 'Basico', 30.00, 'Acceso a instalaciones y clases grupales', '2026-01-01'),
(2, 'Premium', 45.00, 'Acceso ilimitado, clases y entrenador personal', '2026-01-01');

-- =====================================================
-- SALAS FIJAS
-- =====================================================

INSERT INTO sala
(id_sala, nombre, aforo_maximo)
VALUES
(1, 'Sala Agility', 25),
(2, 'Zona Speed', 19),
(3, 'Zona Cross', 12);

-- =====================================================
-- CLASES FIJAS
-- Crossfit -> Zona Cross
-- Yoga, Pilates y Zumba -> Sala Agility
-- Spinning -> Zona Speed
-- =====================================================

INSERT INTO clase
(id_clase, id_entrenador, id_sala, nombre_actividad, calorias_estimadas, dia_semana, hora_inicio, hora_fin, duracion, aforo_maximo, nivel_intensidad)
VALUES
(1, 2, 1, 'Yoga',     200, 'lunes',     '09:00:00', '10:00:00', 60, 20, 'baja'),
(2, 2, 1, 'Pilates',  250, 'martes',    '10:00:00', '11:00:00', 60, 20, 'baja'),
(3, 2, 2, 'Spinning', 450, 'miercoles', '09:00:00', '10:00:00', 60, 19, 'alta'),
(4, 2, 1, 'Zumba',    350, 'jueves',    '10:00:00', '11:00:00', 60, 20, 'media'),
(5, 2, 3, 'Crossfit', 600, 'viernes',   '09:00:00', '10:00:00', 60, 12, 'alta');

-- =====================================================
-- COMPROBACIÓN RÁPIDA
-- =====================================================

SHOW TABLES;
SELECT * FROM clientes;
SELECT * FROM menor;
SELECT * FROM adulto;
SELECT * FROM entrenador;
SELECT * FROM recepcionista;
SELECT * FROM contable;
SELECT * FROM clase;
SELECT * FROM inscripcion;
SELECT * FROM cliente_tarifa;
SELECT * FROM pago;
SELECT * FROM asistencia;
SELECT * FROM registro_acceso;
SELECT * FROM informe;
SELECT * FROM administrador;
SELECT * FROM  empleados;
SELECT * FROM roles;
SELECT * FROM sala;
SELECT * FROM salario_trabajador;
SELECT * FROM tarifa;
SELECT * FROM usuarios;