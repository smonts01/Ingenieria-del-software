-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: stayfit_database
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `stayfit_database`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `stayfit_database` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `stayfit_database`;

--
-- Table structure for table `administrador`
--

DROP TABLE IF EXISTS `administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrador` (
  `id_administrador` int NOT NULL,
  PRIMARY KEY (`id_administrador`),
  CONSTRAINT `fk_administrador_empleado` FOREIGN KEY (`id_administrador`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrador`
--

LOCK TABLES `administrador` WRITE;
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
INSERT INTO `administrador` VALUES (1);
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adulto`
--

DROP TABLE IF EXISTS `adulto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adulto` (
  `id_cliente` int NOT NULL,
  PRIMARY KEY (`id_cliente`),
  CONSTRAINT `fk_adulto_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adulto`
--

LOCK TABLES `adulto` WRITE;
/*!40000 ALTER TABLE `adulto` DISABLE KEYS */;
INSERT INTO `adulto` VALUES (6);
/*!40000 ALTER TABLE `adulto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asistencia`
--

DROP TABLE IF EXISTS `asistencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asistencia` (
  `id_asistencia` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_clase` int NOT NULL,
  `fecha` date NOT NULL,
  `presente` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_asistencia`),
  KEY `fk_asistencia_cliente` (`id_cliente`),
  KEY `fk_asistencia_clase` (`id_clase`),
  CONSTRAINT `fk_asistencia_clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_asistencia_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_asistencia_presente` CHECK ((`presente` in (_utf8mb4'si',_utf8mb4'no')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asistencia`
--

LOCK TABLES `asistencia` WRITE;
/*!40000 ALTER TABLE `asistencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `asistencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clase`
--

DROP TABLE IF EXISTS `clase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clase` (
  `id_clase` int NOT NULL AUTO_INCREMENT,
  `id_entrenador` int NOT NULL,
  `id_sala` int NOT NULL,
  `nombre_actividad` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `calorias_estimadas` int NOT NULL DEFAULT '0',
  `dia_semana` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `duracion` int NOT NULL,
  `aforo_maximo` int NOT NULL,
  `nivel_intensidad` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_clase`),
  KEY `fk_clase_entrenador` (`id_entrenador`),
  KEY `fk_clase_sala` (`id_sala`),
  CONSTRAINT `fk_clase_entrenador` FOREIGN KEY (`id_entrenador`) REFERENCES `entrenador` (`id_entrenador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_clase_sala` FOREIGN KEY (`id_sala`) REFERENCES `sala` (`id_sala`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_clase_aforo` CHECK ((`aforo_maximo` > 0)),
  CONSTRAINT `chk_clase_calorias` CHECK ((`calorias_estimadas` >= 0)),
  CONSTRAINT `chk_clase_duracion` CHECK ((`duracion` > 0)),
  CONSTRAINT `chk_clase_horas` CHECK ((`hora_fin` > `hora_inicio`)),
  CONSTRAINT `chk_clase_nivel` CHECK ((`nivel_intensidad` in (_utf8mb4'baja',_utf8mb4'media',_utf8mb4'alta')))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clase`
--

LOCK TABLES `clase` WRITE;
/*!40000 ALTER TABLE `clase` DISABLE KEYS */;
INSERT INTO `clase` VALUES (1,2,1,'Yoga',200,'lunes','09:00:00','10:00:00',60,20,'media'),(2,2,1,'Pilates',250,'martes','10:00:00','11:00:00',60,20,'baja'),(3,2,2,'Spinning',450,'miercoles','09:00:00','10:00:00',60,19,'alta'),(4,2,1,'Zumba',350,'jueves','10:00:00','11:00:00',60,20,'media'),(5,2,3,'Crossfit',600,'viernes','09:00:00','10:00:00',60,12,'alta');
/*!40000 ALTER TABLE `clase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente_tarifa`
--

DROP TABLE IF EXISTS `cliente_tarifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente_tarifa` (
  `id_cliente_tarifa` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_tarifa` int NOT NULL,
  `fecha_contratacion` date NOT NULL DEFAULT (curdate()),
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'activa',
  PRIMARY KEY (`id_cliente_tarifa`),
  KEY `fk_cliente_tarifa_cliente` (`id_cliente`),
  KEY `fk_cliente_tarifa_tarifa` (`id_tarifa`),
  CONSTRAINT `fk_cliente_tarifa_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_cliente_tarifa_tarifa` FOREIGN KEY (`id_tarifa`) REFERENCES `tarifa` (`id_tarifa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_cliente_tarifa_estado` CHECK ((`estado` in (_utf8mb4'activa',_utf8mb4'cancelada')))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente_tarifa`
--

LOCK TABLES `cliente_tarifa` WRITE;
/*!40000 ALTER TABLE `cliente_tarifa` DISABLE KEYS */;
INSERT INTO `cliente_tarifa` VALUES (1,5,1,'2026-06-06','activa'),(2,6,2,'2026-06-06','activa');
/*!40000 ALTER TABLE `cliente_tarifa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL,
  `estado_pagado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pendiente',
  `calorias_acumuladas` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_cliente`),
  CONSTRAINT `fk_cliente_usuario` FOREIGN KEY (`id_cliente`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_cliente_calorias` CHECK ((`calorias_acumuladas` >= 0)),
  CONSTRAINT `chk_cliente_estado_pagado` CHECK ((`estado_pagado` in (_utf8mb4'abonado',_utf8mb4'pendiente')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (5,'pendiente',0),(6,'pendiente',0);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contable`
--

DROP TABLE IF EXISTS `contable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contable` (
  `id_contable` int NOT NULL,
  `id_administrador_registra` int NOT NULL,
  PRIMARY KEY (`id_contable`),
  KEY `fk_contable_administrador` (`id_administrador_registra`),
  CONSTRAINT `fk_contable_administrador` FOREIGN KEY (`id_administrador_registra`) REFERENCES `administrador` (`id_administrador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_contable_empleado` FOREIGN KEY (`id_contable`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contable`
--

LOCK TABLES `contable` WRITE;
/*!40000 ALTER TABLE `contable` DISABLE KEYS */;
INSERT INTO `contable` VALUES (4,1);
/*!40000 ALTER TABLE `contable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `id_empleado` int NOT NULL,
  `salario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_empleado`),
  CONSTRAINT `fk_empleado_usuario` FOREIGN KEY (`id_empleado`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_empleado_salario` CHECK ((`salario` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
INSERT INTO `empleados` VALUES (1,2000.00),(2,1600.00),(3,0.00),(4,0.00);
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrenador`
--

DROP TABLE IF EXISTS `entrenador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrenador` (
  `id_entrenador` int NOT NULL,
  `id_administrador_registra` int NOT NULL,
  PRIMARY KEY (`id_entrenador`),
  KEY `fk_entrenador_administrador` (`id_administrador_registra`),
  CONSTRAINT `fk_entrenador_administrador` FOREIGN KEY (`id_administrador_registra`) REFERENCES `administrador` (`id_administrador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_entrenador_empleado` FOREIGN KEY (`id_entrenador`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrenador`
--

LOCK TABLES `entrenador` WRITE;
/*!40000 ALTER TABLE `entrenador` DISABLE KEYS */;
INSERT INTO `entrenador` VALUES (2,1);
/*!40000 ALTER TABLE `entrenador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informe`
--

DROP TABLE IF EXISTS `informe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `informe` (
  `id_informe` int NOT NULL AUTO_INCREMENT,
  `id_contable` int NOT NULL,
  `tipo_informe` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_generacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_informe`),
  KEY `fk_informe_contable` (`id_contable`),
  CONSTRAINT `fk_informe_contable` FOREIGN KEY (`id_contable`) REFERENCES `contable` (`id_contable`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informe`
--

LOCK TABLES `informe` WRITE;
/*!40000 ALTER TABLE `informe` DISABLE KEYS */;
/*!40000 ALTER TABLE `informe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscripcion`
--

DROP TABLE IF EXISTS `inscripcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscripcion` (
  `id_inscripcion` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_clase` int NOT NULL,
  `fecha_inscripcion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'inscrito',
  PRIMARY KEY (`id_inscripcion`),
  UNIQUE KEY `uq_cliente_clase` (`id_cliente`,`id_clase`),
  KEY `fk_inscripcion_clase` (`id_clase`),
  CONSTRAINT `fk_inscripcion_clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_inscripcion_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_inscripcion_estado` CHECK ((`estado` in (_utf8mb4'inscrito',_utf8mb4'cancelado')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscripcion`
--

LOCK TABLES `inscripcion` WRITE;
/*!40000 ALTER TABLE `inscripcion` DISABLE KEYS */;
/*!40000 ALTER TABLE `inscripcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menor`
--

DROP TABLE IF EXISTS `menor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menor` (
  `id_cliente` int NOT NULL,
  `dni_tutor` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_tutor` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_cliente`),
  CONSTRAINT `fk_menor_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menor`
--

LOCK TABLES `menor` WRITE;
/*!40000 ALTER TABLE `menor` DISABLE KEYS */;
INSERT INTO `menor` VALUES (5,'77788996J','Ana');
/*!40000 ALTER TABLE `menor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_contable` int NOT NULL,
  `id_tarifa` int NOT NULL,
  `importe` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_pago` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_pago`),
  KEY `fk_pago_cliente` (`id_cliente`),
  KEY `fk_pago_contable` (`id_contable`),
  KEY `fk_pago_tarifa` (`id_tarifa`),
  CONSTRAINT `fk_pago_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_pago_contable` FOREIGN KEY (`id_contable`) REFERENCES `contable` (`id_contable`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_pago_tarifa` FOREIGN KEY (`id_tarifa`) REFERENCES `tarifa` (`id_tarifa`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_pago_importe` CHECK ((`importe` > 0)),
  CONSTRAINT `chk_pago_metodo` CHECK ((`metodo_pago` in (_utf8mb4'efectivo',_utf8mb4'tarjeta',_utf8mb4'transferencia',_utf8mb4'bizum')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pago`
--

LOCK TABLES `pago` WRITE;
/*!40000 ALTER TABLE `pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recepcionista`
--

DROP TABLE IF EXISTS `recepcionista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recepcionista` (
  `id_recepcionista` int NOT NULL,
  `id_administrador_registra` int NOT NULL,
  PRIMARY KEY (`id_recepcionista`),
  KEY `fk_recepcionista_administrador` (`id_administrador_registra`),
  CONSTRAINT `fk_recepcionista_administrador` FOREIGN KEY (`id_administrador_registra`) REFERENCES `administrador` (`id_administrador`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_recepcionista_empleado` FOREIGN KEY (`id_recepcionista`) REFERENCES `empleados` (`id_empleado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recepcionista`
--

LOCK TABLES `recepcionista` WRITE;
/*!40000 ALTER TABLE `recepcionista` DISABLE KEYS */;
/*!40000 ALTER TABLE `recepcionista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registro_acceso`
--

DROP TABLE IF EXISTS `registro_acceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registro_acceso` (
  `id_registro` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha_hora_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo_acceso` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_registro`),
  KEY `fk_registro_acceso_usuario` (`id_usuario`),
  CONSTRAINT `fk_registro_acceso_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_registro_tipo_acceso` CHECK ((`tipo_acceso` in (_utf8mb4'entrada',_utf8mb4'salida')))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registro_acceso`
--

LOCK TABLES `registro_acceso` WRITE;
/*!40000 ALTER TABLE `registro_acceso` DISABLE KEYS */;
INSERT INTO `registro_acceso` VALUES (1,6,'2026-06-06 16:00:08','entrada'),(2,6,'2026-06-06 16:00:09','salida');
/*!40000 ALTER TABLE `registro_acceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre_rol` (`nombre_rol`),
  CONSTRAINT `chk_roles_nombre` CHECK ((`nombre_rol` in (_utf8mb4'cliente',_utf8mb4'entrenador',_utf8mb4'recepcionista',_utf8mb4'administrador',_utf8mb4'contable')))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (4,'administrador'),(1,'cliente'),(5,'contable'),(2,'entrenador'),(3,'recepcionista');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sala`
--

DROP TABLE IF EXISTS `sala`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sala` (
  `id_sala` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `aforo_maximo` int NOT NULL,
  PRIMARY KEY (`id_sala`),
  UNIQUE KEY `nombre` (`nombre`),
  CONSTRAINT `chk_sala_aforo` CHECK ((`aforo_maximo` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sala`
--

LOCK TABLES `sala` WRITE;
/*!40000 ALTER TABLE `sala` DISABLE KEYS */;
INSERT INTO `sala` VALUES (1,'Sala Agility',25),(2,'Zona Speed',19),(3,'Zona Cross',12);
/*!40000 ALTER TABLE `sala` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salario_trabajador`
--

DROP TABLE IF EXISTS `salario_trabajador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salario_trabajador` (
  `id_salario` int NOT NULL AUTO_INCREMENT,
  `id_rol` int NOT NULL,
  `nombre_puesto` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `salario_base` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_salario`),
  UNIQUE KEY `id_rol` (`id_rol`),
  UNIQUE KEY `nombre_puesto` (`nombre_puesto`),
  CONSTRAINT `fk_salario_trabajador_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_salario_base` CHECK ((`salario_base` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salario_trabajador`
--

LOCK TABLES `salario_trabajador` WRITE;
/*!40000 ALTER TABLE `salario_trabajador` DISABLE KEYS */;
INSERT INTO `salario_trabajador` VALUES (1,2,'entrenador',1600.00),(2,3,'recepcionista',1200.00),(3,4,'administrador',2000.00),(4,5,'contable',1800.00);
/*!40000 ALTER TABLE `salario_trabajador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tarifa`
--

DROP TABLE IF EXISTS `tarifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarifa` (
  `id_tarifa` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio_mensual` decimal(10,2) NOT NULL,
  `servicios_incluidos` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_inicio` date NOT NULL,
  PRIMARY KEY (`id_tarifa`),
  UNIQUE KEY `nombre` (`nombre`),
  CONSTRAINT `chk_tarifa_precio` CHECK ((`precio_mensual` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarifa`
--

LOCK TABLES `tarifa` WRITE;
/*!40000 ALTER TABLE `tarifa` DISABLE KEYS */;
INSERT INTO `tarifa` VALUES (1,'Basico',30.00,'Acceso a instalaciones y clases grupales','2026-01-01'),(2,'Premium',45.00,'Acceso ilimitado, clases y entrenador personal','2026-01-01');
/*!40000 ALTER TABLE `tarifa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `dni` varchar(9) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_rol` int NOT NULL,
  `direccion` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_nacimiento` date NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `dni` (`dni`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_usuario_rol` (`id_rol`),
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'00000001A','Admin Principal','600000001','admin@stayfit.com','admin','admin1',4,'Calle Admin 1','2026-06-06 14:26:45','1980-01-01'),(2,'00000002B','Entrenador Principal','600000002','entrenador@stayfit.com','entrenador','entrenador1',2,'Calle Entrenador 1','2026-06-06 14:26:45','1990-02-02'),(3,'11111111K','Recepcionista principal','444555666','recepcionista@gmail.com','recepcionista','dd9485cfacee1e3da810c678c92901f30ac48f22ee859e77ddf6213e521cca40',3,'Calle 3','2026-06-06 15:11:51','2000-07-01'),(4,'55555555L','Contable Principal','666555777','contable@gmail.com','contable','40fc8c4faec03f77999287695c59455a72e34b263b2ebea40999298974a75b0a',5,'Calle 2','2026-06-06 15:12:34','2000-10-01'),(5,'44444444L','Andrea','888999444','andrea@gmail.com','andrea','41d42da01baa7b1fb1b8b926b294e7ae31920596e176f81dc2701a1d65b887fa',1,'Calle 33','2026-06-06 15:59:06','1978-05-01'),(6,'55555555J','Sonia','444555666','sonia@gmail.com','sonia','bd4ff2fd93a94793657f95f540289ccd658c7231ea64c0b6eaa442b4ab493d96',1,'Calle 67','2026-06-06 15:59:44','2006-07-25');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'stayfit_database'
--

--
-- Dumping routines for database 'stayfit_database'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-06 16:00:25
