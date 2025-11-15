-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: db_artesanias
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `fecha_agregado` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `carrito_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (10,5,74,1,'2025-11-13 04:55:08'),(20,1,7,1,'2025-11-14 18:06:59'),(21,1,41,2,'2025-11-14 18:07:12'),(22,1,11,2,'2025-11-14 19:35:36'),(23,1,4,2,'2025-11-14 19:35:39'),(24,1,31,1,'2025-11-14 19:36:29'),(25,1,22,1,'2025-11-14 23:03:05'),(26,1,60,1,'2025-11-14 23:03:41'),(27,1,2,1,'2025-11-14 23:04:20'),(28,1,47,1,'2025-11-15 04:14:55'),(29,1,52,1,'2025-11-15 04:15:01');
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `activa` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Joyería','Accesorios artesanales en metal y materiales naturales',1),(2,'Accesorios','Accesorios personales de uso decorativo',1),(3,'Cerámica','Piezas elaboradas con arcilla artesanal del Chocó',1),(4,'Madera','Artesanías y objetos elaborados en madera',1);
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` VALUES (1,2,9,2,90000.00,180000.00),(2,2,13,1,3000.00,3000.00),(3,2,1,2,25000.00,50000.00),(4,3,72,1,160000.00,160000.00),(5,3,67,1,110000.00,110000.00),(6,3,68,1,115000.00,115000.00),(7,3,33,1,150000.00,150000.00),(8,3,39,1,150000.00,150000.00),(9,4,73,1,90000.00,90000.00),(10,4,68,1,115000.00,115000.00),(11,4,35,1,175000.00,175000.00),(12,4,39,2,150000.00,300000.00),(13,4,36,1,225000.00,225000.00),(14,4,4,2,120000.00,240000.00),(15,4,2,2,85000.00,170000.00),(16,4,11,4,80000.00,320000.00);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagenes`
--

DROP TABLE IF EXISTS `imagenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `tipo` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ancho` int DEFAULT NULL,
  `alto` int DEFAULT NULL,
  `ruta` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_carga` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `imagenes_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes`
--

LOCK TABLES `imagenes` WRITE;
/*!40000 ALTER TABLE `imagenes` DISABLE KEYS */;
INSERT INTO `imagenes` VALUES (1,11,'image/jpg',1024,768,'media/aretes1.jpg','2025-11-12 21:14:35'),(2,4,'image/jpg',1024,768,'media/aretes2.jpg','2025-11-12 21:14:35'),(3,1,'image/jpg',1024,768,'media/aretes3.jpg','2025-11-12 21:14:35'),(4,2,'image/jpg',1024,768,'media/aretes4.jpg','2025-11-12 21:14:35'),(5,7,'image/jpg',1024,768,'media/aretes5.jpg','2025-11-12 21:14:35'),(6,8,'image/jpg',1024,768,'media/aretes6.jpg','2025-11-12 21:14:35'),(7,10,'image/jpg',1024,768,'media/aretes7.jpg','2025-11-12 21:14:35'),(8,6,'image/jpg',1024,768,'media/aretes8.jpg','2025-11-12 21:14:35'),(9,5,'image/jpg',1024,768,'media/aretes9.jpg','2025-11-12 21:14:35'),(10,9,'image/jpg',1024,768,'media/aretes10.jpg','2025-11-12 21:14:35'),(11,12,'image/jpg',1024,768,'media/manillas1.jpg','2025-11-12 23:26:44'),(12,13,'image/jpg',1024,768,'media/manillas2.jpg','2025-11-12 23:26:44'),(13,16,'image/jpg',1024,768,'media/manillas3.jpg','2025-11-12 23:26:44'),(14,22,'image/jpg',1024,768,'media/manillas4.jpg','2025-11-12 23:26:44'),(15,21,'image/jpg',1024,768,'media/manillas5.jpg','2025-11-12 23:26:44'),(16,18,'image/jpg',1024,768,'media/manillas6.jpg','2025-11-12 23:26:44'),(17,19,'image/jpg',1024,768,'media/manillas7.jpg','2025-11-12 23:26:44'),(18,15,'image/jpg',1024,768,'media/manillas8.jpg','2025-11-12 23:26:44'),(19,20,'image/jpg',1024,768,'media/manillas9.jpg','2025-11-12 23:26:44'),(20,17,'image/jpg',1024,768,'media/manillas10.jpg','2025-11-12 23:26:44'),(21,23,'image/jpg',1024,768,'media/collares1.jpg','2025-11-13 00:22:35'),(22,24,'image/jpg',1024,768,'media/collares2.jpg','2025-11-13 00:22:35'),(23,25,'image/jpg',1024,768,'media/collares3.jpg','2025-11-13 00:22:35'),(24,26,'image/jpg',1024,768,'media/collares4.jpg','2025-11-13 00:22:35'),(25,27,'image/jpg',1024,768,'media/collares5.jpg','2025-11-13 00:22:35'),(26,28,'image/jpg',1024,768,'media/collares6.jpg','2025-11-13 00:22:35'),(27,29,'image/jpg',1024,768,'media/collares7.jpg','2025-11-13 00:22:35'),(28,30,'image/jpg',1024,768,'media/collares8.jpg','2025-11-13 00:22:35'),(29,31,'image/jpg',1024,768,'media/collares9.jpg','2025-11-13 00:22:35'),(30,32,'image/jpg',1024,768,'media/collares10.jpg','2025-11-13 00:22:35'),(31,33,'image/jpg',1024,768,'media/bolsos1.jpg','2025-11-13 00:50:32'),(32,34,'image/jpg',1024,768,'media/bolsos2.jpg','2025-11-13 00:50:32'),(33,35,'image/jpg',1024,768,'media/bolsos3.jpg','2025-11-13 00:50:32'),(34,36,'image/jpg',1024,768,'media/bolsos4.jpg','2025-11-13 00:50:32'),(35,37,'image/jpg',1024,768,'media/bolsos5.jpg','2025-11-13 00:50:32'),(36,38,'image/jpg',1024,768,'media/bolsos6.jpg','2025-11-13 00:50:32'),(37,39,'image/jpg',1024,768,'media/bolsos7.jpg','2025-11-13 00:50:32'),(38,40,'image/jpg',1024,768,'media/bolsos8.jpg','2025-11-13 00:50:32'),(39,41,'image/jpg',1024,768,'media/bolsos9.jpg','2025-11-13 00:50:32'),(40,42,'image/jpg',1024,768,'media/bolsos10.jpg','2025-11-13 00:50:32'),(41,43,'image/jpg',1024,768,'media/sombreros1.jpg','2025-11-13 01:29:51'),(42,44,'image/jpg',1024,768,'media/sombreros2.jpg','2025-11-13 01:29:51'),(43,45,'image/jpg',1024,768,'media/sombreros3.jpg','2025-11-13 01:29:51'),(44,46,'image/jpg',1024,768,'media/sombreros4.jpg','2025-11-13 01:29:51'),(45,47,'image/jpg',1024,768,'media/sombreros5.jpg','2025-11-13 01:29:51'),(46,48,'image/jpg',1024,768,'media/sombreros6.jpg','2025-11-13 01:29:51'),(47,49,'image/jpg',1024,768,'media/sombreros7.jpg','2025-11-13 01:29:51'),(48,50,'image/jpg',1024,768,'media/sombreros8.jpg','2025-11-13 01:29:51'),(49,51,'image/jpg',1024,768,'media/sombreros9.jpg','2025-11-13 01:29:51'),(50,52,'image/jpg',1024,768,'media/sombreros10.jpg','2025-11-13 01:29:51'),(51,53,'image/jpg',1024,768,'media/turbantes1.jpg','2025-11-13 02:14:15'),(52,54,'image/jpg',1024,768,'media/turbantes2.jpg','2025-11-13 02:14:15'),(53,55,'image/jpg',1024,768,'media/turbantes3.jpg','2025-11-13 02:14:15'),(54,56,'image/jpg',1024,768,'media/turbantes4.jpg','2025-11-13 02:14:15'),(55,57,'image/jpg',1024,768,'media/turbantes5.jpg','2025-11-13 02:14:15'),(56,58,'image/jpg',1024,768,'media/turbantes6.jpg','2025-11-13 02:14:15'),(57,59,'image/jpg',1024,768,'media/turbantes7.jpg','2025-11-13 02:14:15'),(58,60,'image/jpg',1024,768,'media/turbantes8.jpg','2025-11-13 02:14:15'),(59,61,'image/jpg',1024,768,'media/turbantes9.jpg','2025-11-13 02:14:15'),(60,62,'image/jpg',1024,768,'media/turbantes10.jpg','2025-11-13 02:14:15'),(61,63,'image/jpg',1024,768,'media/ceramicas1.jpg','2025-11-13 02:56:15'),(62,64,'image/jpg',1024,768,'media/ceramicas2.jpg','2025-11-13 02:56:15'),(63,65,'image/jpg',1024,768,'media/ceramicas3.jpg','2025-11-13 02:56:15'),(64,66,'image/jpg',1024,768,'media/ceramicas4.jpg','2025-11-13 02:56:15'),(65,67,'image/jpg',1024,768,'media/ceramicas5.jpg','2025-11-13 02:56:15'),(66,68,'image/jpg',1024,768,'media/ceramicas6.jpg','2025-11-13 02:56:15'),(67,69,'image/jpg',1024,768,'media/ceramicas7.jpg','2025-11-13 02:56:15'),(68,70,'image/jpg',1024,768,'media/ceramicas8.jpg','2025-11-13 02:56:15'),(69,71,'image/jpg',1024,768,'media/ceramicas9.jpg','2025-11-13 02:56:15'),(70,72,'image/jpg',1024,768,'media/ceramicas10.jpg','2025-11-13 02:56:15'),(71,73,'image/jpg',1024,768,'media/ebanisteria1.jpg','2025-11-13 04:26:00'),(72,74,'image/jpg',1024,768,'media/ebanisteria2.jpg','2025-11-13 04:26:00'),(73,75,'image/jpg',1024,768,'media/ebanisteria3.jpg','2025-11-13 04:26:00'),(74,76,'image/jpg',1024,768,'media/ebanisteria4.jpg','2025-11-13 04:26:00'),(75,77,'image/jpg',1024,768,'media/ebanisteria5.jpg','2025-11-13 04:26:00'),(76,78,'image/jpg',1024,768,'media/ebanisteria6.jpg','2025-11-13 04:26:00'),(77,79,'image/jpg',1024,768,'media/ebanisteria7.jpg','2025-11-13 04:26:00'),(78,80,'image/jpg',1024,768,'media/ebanisteria8.jpg','2025-11-13 04:26:00'),(79,80,'image/jpeg',1440,1920,'media\\40908156d6894b3c92816c12362c1870.jpeg','2025-11-12 05:00:00');
/*!40000 ALTER TABLE `imagenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','confirmado','en_proceso','enviado','entregado','cancelado') COLLATE utf8mb4_general_ci DEFAULT 'pendiente',
  `fecha_pedido` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `direccion_envio` text COLLATE utf8mb4_general_ci,
  `telefono_contacto` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,95000.00,'confirmado','2025-11-05 03:29:00','Quibdó, Chocó - Barrio Jardín','3105558899'),(2,1,233000.00,'pendiente','2025-11-12 14:41:10','Argentina','3103333333'),(3,1,685000.00,'pendiente','2025-11-13 04:42:45','Buenaventura','32222222'),(4,1,1635000.00,'pendiente','2025-11-14 18:06:48','Pereira','3222222222');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `precio` decimal(10,2) NOT NULL,
  `precio_anterior` decimal(10,2) DEFAULT NULL,
  `subcategoria_id` int DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT '0.00',
  `reviews` int DEFAULT '0',
  `stock` int DEFAULT '0',
  `artesano_id` int DEFAULT NULL,
  `destacado` tinyint(1) DEFAULT '0',
  `activo` tinyint(1) DEFAULT '1',
  `fecha_creacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `artesano_id` (`artesano_id`),
  KEY `subcategoria_id` (`subcategoria_id`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`artesano_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`subcategoria_id`) REFERENCES `subcategorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Aretes Oro Espiral','Aretes artesanales con chaquiras doradas en diseño espiral.',150000.00,NULL,1,0.00,0,68,2,0,1,'2025-11-09 20:47:20'),(2,'Aretes Ballena Miyuki','Aretes en miyuki con diseño de ballena, coloridos y hechos a mano.',85000.00,NULL,1,0.00,0,28,2,0,1,'2025-11-09 20:47:20'),(3,'Aretes Mujer Afro en cristal de Miyuki','Aretes de mujer afro elaborados a mano con cristales de miyuki.',65000.00,NULL,1,0.00,0,20,2,0,0,'2025-11-09 20:47:20'),(4,'Aretes Afrrochocó','Aretes Afrochocó hechos a mano, inspirados en la cultura del Pacífico.',120000.00,NULL,1,0.00,0,20,2,0,1,'2025-11-09 20:47:20'),(5,'Aretes Mapa del Chocó','Aretes con diseño del mapa del Chocó, elaborados a mano con detalle artesanal.',100000.00,NULL,1,0.00,0,40,2,1,1,'2025-11-09 20:47:20'),(6,'Aretes Mandala','Aretes mandala hechos a mano con chaquiras, llenos de color y armonía.',40000.00,NULL,1,0.00,0,60,2,0,1,'2025-11-09 20:47:20'),(7,'Aretes en Oro Con Hilo metalizado','Arete en oro tejido con hilo metalizado, elegante y artesanal.',70000.00,NULL,1,0.00,0,25,2,0,0,'2025-11-09 20:47:20'),(8,'Aretes Mapa de Africa','Aretes con mapa de África pintado a mano, llenos de color y cultura.',150000.00,NULL,1,0.00,0,10,2,0,1,'2025-11-09 20:47:20'),(9,'Aretes Flor Mandala','Aretes flor de mandala hechos a mano, coloridos y llenos de armonía.',90000.00,NULL,1,0.00,0,16,2,0,1,'2025-11-09 20:47:20'),(10,'Aretes Iracan','Elaborado con palma de iraca.',55000.00,NULL,1,0.00,0,35,2,0,1,'2025-11-09 20:47:20'),(11,'Aretes Afrochocó','Aretes Afrochocó hechos a mano, inspirados en la cultura del Pacífico.',80000.00,NULL,1,0.00,0,4,2,0,1,'2025-11-09 20:47:20'),(12,'Manillla miyuki de corazón','Manilla Miyuki de corazones. Pulsera artesanal, delicada y colorida.',40000.00,NULL,2,0.00,0,50,2,0,1,'2025-11-09 20:47:20'),(13,'Manilla Miyuki de Colores','Pulsera artesanal tejida a mano.',3000.00,NULL,2,0.00,0,4,2,0,1,'2025-11-11 06:45:10'),(14,'Manilla miyuki de la virgen','Manillas personalizadas con chaquiras.',20000.00,NULL,2,0.00,0,10,2,0,0,'2025-11-12 08:20:47'),(15,'Manilla tejida de Unicornio','Manillaa tejia personalizada con accesorios.',45000.00,NULL,2,0.00,0,25,2,0,1,'2025-11-12 15:44:01'),(16,'SeT de manillas de 3 Miyuki con chaquiras','Juego de tres manillas elaboradas con chaquiras Miyuki finas, combinadas en diseños coloridos y elegantes.',20000.00,NULL,2,0.00,0,20,2,0,1,'2025-11-12 23:00:52'),(17,'Manillas Miyuki mostacillas chaquiras','Manilla artesanal tejida con mostacillas y chaquiras Miyuki, ideal para un toque moderno y artesanal.',35000.00,NULL,2,0.00,0,25,2,0,1,'2025-11-12 23:00:52'),(18,'Manillas de flor y mariposas Miyuki chaquiras','Delicadas manillas con diseños de flores y mariposas tejidas en chaquiras Miyuki, llenas de color y detalle.',50000.00,NULL,2,0.00,0,18,2,0,1,'2025-11-12 23:00:52'),(19,'Manillas multicolor redonda','Manilla redonda con combinación de chaquiras multicolor, perfecta para un estilo alegre y juvenil.',20000.00,NULL,2,0.00,0,30,2,0,1,'2025-11-12 23:00:52'),(20,'SecT manillas Miyuki en oro con chaquiras','Set de manillas Miyuki con detalles dorados y chaquiras brillantes, un diseño sofisticado y artesanal.',25000.00,NULL,2,0.00,0,15,2,1,1,'2025-11-12 23:00:52'),(21,'Manillas Miyuki tejidas de colores','Manilla tejida a mano con chaquiras Miyuki de colores vivos, reflejando arte y tradición en cada pieza.',18000.00,NULL,2,0.00,0,22,2,0,1,'2025-11-12 23:00:52'),(22,'Manilla de la virgen','Manillas personalizadas con chaquiras.',25000.00,NULL,2,0.00,0,20,2,0,1,'2025-11-12 23:31:18'),(23,'Collar en degradés en chaquiras','Collar artesanal con chaquiras dispuestas en tonos degradados que crean un efecto elegante y moderno.',70000.00,NULL,3,0.00,0,20,2,0,1,'2025-11-13 00:17:45'),(24,'Collar girasol en chaquiras','Collar tejido a mano con diseño de girasol en chaquiras, lleno de color y energía natural.',75000.00,NULL,3,0.00,0,18,2,0,1,'2025-11-13 00:17:45'),(25,'Collar okama en chaquiras','Collar tradicional tipo okama elaborado con chaquiras finas, símbolo de identidad y arte ancestral.',10000.00,NULL,3,0.00,0,15,2,0,1,'2025-11-13 00:17:45'),(26,'Collar África','Collar inspirado en la cultura africana, con colores vibrantes y diseño que refleja raíces étnicas.',65000.00,NULL,3,0.00,0,22,2,0,1,'2025-11-13 00:17:45'),(27,'Collar en V con chaquiras','Collar artesanal con forma de “V”, tejido con chaquiras de colores que realzan el escote con elegancia.',58000.00,NULL,3,0.00,0,25,2,0,1,'2025-11-13 00:17:45'),(28,'Collar mandala en chaquira','Collar circular con diseño de mandala hecho en chaquiras, representando armonía y equilibrio.',122000.00,NULL,3,0.00,0,17,2,1,1,'2025-11-13 00:17:45'),(29,'Collar en acero mapa del Chocó','Collar en acero inoxidable con dije del mapa del Chocó, símbolo de orgullo y pertenencia.',80000.00,NULL,3,0.00,0,30,2,0,1,'2025-11-13 00:17:45'),(30,'Collar en acero de colores','Collar moderno en acero con detalles coloridos, ideal para un estilo contemporáneo y alegre.',82000.00,NULL,3,0.00,0,28,2,0,1,'2025-11-13 00:17:45'),(31,'Collar de caurí','Collar decorado con conchas caurí, evocando la conexión con el mar y la cultura afrocolombiana.',55000.00,NULL,3,0.00,0,26,2,0,1,'2025-11-13 00:17:45'),(32,'Collar Okama rombo multicolor','Collar tipo okama con patrón de rombos en chaquiras multicolor, vibrante y lleno de detalle artesanal.',150000.00,NULL,3,0.00,0,16,2,0,1,'2025-11-13 00:17:45'),(33,'Bolso yoyo manos libre iraca','Bolso tipo yoyo tejido en palma de iraca, práctico y elegante para uso diario.',150000.00,NULL,4,0.00,0,14,2,0,1,'2025-11-13 00:46:31'),(34,'Bolso figura en iraca','Bolso artesanal con diseño de figura tejida en iraca, mezcla de tradición y estilo.',170000.00,NULL,4,0.00,0,18,2,0,1,'2025-11-13 00:46:31'),(35,'Bolso figura en iraca multicolor','Bolso colorido hecho a mano en palma de iraca, con figuras vibrantes y alegres.',175000.00,NULL,4,0.00,0,19,2,0,1,'2025-11-13 00:46:31'),(36,'Bolso trenzado en iraca','Bolso trenzado a mano con palma de iraca natural, resistente y con diseño único.',225000.00,NULL,4,0.00,0,16,2,0,1,'2025-11-13 00:46:31'),(37,'Bolso yoyo en iraca con flores','Bolso artesanal tipo yoyo decorado con flores en iraca, delicado y femenino.',150000.00,NULL,4,0.00,0,12,2,1,1,'2025-11-13 00:46:31'),(38,'Bolso carrete de iraca','Bolso circular tejido con técnica de carrete en palma de iraca, moderno y artesanal.',115000.00,NULL,4,0.00,0,14,2,0,1,'2025-11-13 00:46:31'),(39,'Bolso mochila en palma iraca','Mochila artesanal elaborada en palma de iraca, práctica, fresca y duradera.',150000.00,NULL,4,0.00,0,7,2,0,1,'2025-11-13 00:46:31'),(40,'Bolso exagonal en iraca','Bolso con forma hexagonal tejido en palma de iraca, diseño geométrico y elegante.',135000.00,NULL,4,0.00,0,16,2,0,1,'2025-11-13 00:46:31'),(41,'Bolso bercan negro y naranja','Bolso artesanal en tonos negro y naranja, tejido en iraca con estilo vibrante y moderno.',145000.00,NULL,4,0.00,0,13,2,0,1,'2025-11-13 00:46:31'),(42,'Bolso bercan rojo','Bolso en palma de iraca color rojo intenso, pieza artesanal llena de personalidad.',160000.00,NULL,4,0.00,0,11,2,0,1,'2025-11-13 00:46:31'),(43,'Sombrero Amor Tropical','Sombrero de paja decorado con cintas coloridas y detalles alegres, ideal para un look playero.',130000.00,NULL,5,0.00,0,15,2,1,1,'2025-11-13 01:22:33'),(44,'Sombrero Fe Marina','Sombrero en tonos crema y turquesa con borlas suaves y estilo boho chic.',125000.00,NULL,5,0.00,0,18,2,0,1,'2025-11-13 01:22:33'),(45,'Sombrero Cataleya Cowboy','Sombrero calado estilo cowboy, mezcla de elegancia y toque natural.',140000.00,NULL,5,0.00,0,16,2,0,1,'2025-11-13 01:22:33'),(46,'Sombrero Vueltiao Étnico','Sombrero colombiano tejido a mano con diseño tradicional y acabado artesanal.',150000.00,NULL,5,0.00,0,20,2,0,1,'2025-11-13 01:22:33'),(47,'Pamela Personalizada Steph','Sombrero de playa de ala ancha decorado con el nombre Steph y flor pintada.',135000.00,NULL,5,0.00,0,14,2,0,1,'2025-11-13 01:22:33'),(48,'Sombrero Crochet Rústico','Sombrero tejido en fibra natural con cinta tropical y estilo casual.',120000.00,NULL,5,0.00,0,12,2,0,1,'2025-11-13 01:22:33'),(49,'Sombrero Caribe Trenzado','Sombrero trenzado con tonos azules y dorados, adornado con pompones vibrantes.',155000.00,NULL,5,0.00,0,13,2,0,1,'2025-11-13 01:22:33'),(50,'Sombrero Vaquero Boho Chic','Sombrero vaquero tejido a crochet con conchas y detalles coloridos.',145000.00,NULL,5,0.00,0,11,2,0,1,'2025-11-13 01:22:33'),(51,'Sombrero Sabanero Clásico','Sombrero de ala ancha con cordón ajustable, ideal para campo o sol.',125000.00,NULL,5,0.00,0,10,2,0,1,'2025-11-13 01:22:33'),(52,'Sombrero Mayorquina Estilizado','Sombrero clásico con ribete blanco y emblema elegante en la banda.',180000.00,NULL,5,0.00,0,9,2,0,1,'2025-11-13 01:22:33'),(53,'Turbante Rosetón Borgoña','Turbante prearmado color borgoña con diseño floral tejido.',35000.00,NULL,6,0.00,0,40,2,0,1,'2025-11-13 02:09:37'),(54,'Diadema Turbante Floral','Diadema con nudo frontal y estampado floral vibrante.',30000.00,NULL,6,0.00,0,50,2,0,1,'2025-11-13 02:09:37'),(55,'Diadema Nudo Corteza','Diadema con nudo y patrón orgánico en tonos tierra.',32000.00,NULL,6,0.00,0,45,2,0,1,'2025-11-13 02:09:37'),(56,'Turbante Estampado Abstracto','Turbante moderno con amarre lateral y estampado abstracto.',36000.00,NULL,6,0.00,0,35,2,0,1,'2025-11-13 02:09:37'),(57,'Dúo Turbante Cebra y Rosa','Set de dos turbantes: uno cebra y otro rosa estampado.',42000.00,NULL,6,0.00,0,25,2,0,1,'2025-11-13 02:09:37'),(58,'Turbante Nudo Cuadros Vichy','Turbante con nudo superior y estampado Vichy.',34000.00,NULL,6,0.00,0,30,2,0,1,'2025-11-13 02:09:37'),(59,'Diadema Nudo Jardín Pop','Diadema con flores grandes en tonos brillantes.',32000.00,NULL,6,0.00,0,40,2,1,1,'2025-11-13 02:09:37'),(60,'Lazo Grande Satín Floral','Lazo grande de satín con estampado floral colorido.',33000.00,NULL,6,0.00,0,55,2,0,1,'2025-11-13 02:09:37'),(61,'Diadema Nudo Plumas Tropicales','Diadema con estampado de plumas en tonos vivos.',35000.00,NULL,6,0.00,0,50,2,0,1,'2025-11-13 02:09:37'),(62,'Lazo Grande Animal Print Cebra','Lazo grande con estampado clásico de cebra.',31000.00,NULL,6,0.00,0,60,2,0,1,'2025-11-13 02:09:37'),(63,'Tazas con Corazón','Taza con textura moteada y corazón incrustado, incluye plato de gres.',100000.00,NULL,7,0.00,0,20,2,0,1,'2025-11-13 02:52:54'),(64,'Jarrita Flores','Pequeña jarra con borde ondulado y flores pintadas a mano.',105000.00,NULL,7,0.00,0,25,2,0,1,'2025-11-13 02:52:54'),(65,'Set Monogramas','Set de tazas y bandejas de gres con monograma grabado.',120000.00,NULL,7,0.00,0,15,2,0,1,'2025-11-13 02:52:54'),(66,'Set Cerezo en Flor','Set con relieves pintados a mano inspirados en flores de cerezo.',130000.00,NULL,7,0.00,0,18,2,0,1,'2025-11-13 02:52:54'),(67,'Regalo Corazón Rosa','Set con taza y platos en forma de corazón decorados a mano.',110000.00,NULL,7,0.00,0,21,2,0,1,'2025-11-13 02:52:54'),(68,'Bandeja Rayas','Bandeja rayada con flor pintada a mano y pequeños cuencos.',115000.00,NULL,7,0.00,0,18,2,1,1,'2025-11-13 02:52:54'),(69,'Imanes Figuras','Coloridas figuras de cerámica esmaltada ideales como imanes.',100000.00,NULL,7,0.00,0,30,2,0,1,'2025-11-13 02:52:54'),(70,'Platos de Orishas','Trío de bandejas pintadas con figuras femeninas blancas.',140000.00,NULL,7,0.00,0,12,2,0,1,'2025-11-13 02:52:54'),(71,'Platos Corazón Mal de Ojo','Platos en forma de corazón con diseño gráfico rojo y geométrico.',120000.00,NULL,7,0.00,0,15,2,0,1,'2025-11-13 02:52:54'),(72,'Filtro de Agua','Filtro de arcilla en forma de casita decorada con detalles campestres.',160000.00,NULL,7,0.00,0,9,2,0,1,'2025-11-13 02:52:54'),(73,'Tallado Árbol de Colores','Escultura de madera tallada con diseño de árbol multicolor.',90000.00,NULL,8,0.00,0,19,2,0,1,'2025-11-13 04:22:04'),(74,'Tallado de Coliflor','Figura artesanal tallada en madera con forma de coliflor.',85000.00,NULL,8,0.00,0,25,2,1,1,'2025-11-13 04:22:04'),(75,'Tallado Centro de Mesa Floral','Centro tallado con diseño floral elegante y acabado brillante.',95000.00,NULL,8,0.00,0,15,2,0,1,'2025-11-13 04:22:04'),(76,'Tallado de Platos Ondulados','Platos tallados con bordes ondulados y textura rústica.',80000.00,NULL,8,0.00,0,30,2,0,1,'2025-11-13 04:22:04'),(77,'Set de Tallados de Platos y Cuchara','Conjunto artesanal de platos y cuchara tallados en madera.',100000.00,NULL,8,0.00,0,18,2,0,0,'2025-11-13 04:22:04'),(78,'Set de Tallados de Peces','Piezas decorativas talladas a mano con formas de peces.',110000.00,NULL,8,0.00,0,12,2,0,0,'2025-11-13 04:22:04'),(79,'Tallado de Centro de Mesa Natural','Centro de mesa tallado con textura natural y forma orgánica.',9000.00,NULL,8,0.00,0,24,2,0,0,'2025-11-13 04:22:04'),(80,'Tallado Decorativo Central','Figura tallada a mano con diseño artístico y acabado pulido.',95000.00,NULL,8,0.00,0,20,2,0,0,'2025-11-13 04:22:04');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcategorias`
--

DROP TABLE IF EXISTS `subcategorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subcategorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoria_id` int NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `activa` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `subcategorias_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcategorias`
--

LOCK TABLES `subcategorias` WRITE;
/*!40000 ALTER TABLE `subcategorias` DISABLE KEYS */;
INSERT INTO `subcategorias` VALUES (1,1,'Aretes','Aretes artesanales con materiales del pacífico',1),(2,1,'Manillas','Pulseras artesanales africanas y afrocolombianas',1),(3,1,'Collares','Collares hechos a mano con semillas y chaquiras',1),(4,2,'Bolsos','Bolsos y carteras de fibra natural',1),(5,2,'Sombreros','Sombreros típicos y contemporáneos',1),(6,2,'Turbantes','Accesorios textiles para la cabeza',1),(7,3,'Cerámica','Piezas culturales de barro y arcilla',1),(8,4,'Ebanistería','Trabajos tradicionales en madera',1);
/*!40000 ALTER TABLE `subcategorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `clave` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direccion` text COLLATE utf8mb4_general_ci,
  `rol` enum('cliente','artesano','admin') COLLATE utf8mb4_general_ci DEFAULT 'cliente',
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Yajanny Mena','yajanny@example.com','$2b$12$ZD93kFaclofAWVgKGrFLm.YACfDTh3V6tuqIJqY.JpQffIl1In.uS','3105558899','Quibdó, Chocó','cliente','2025-11-05 03:29:00',1),(2,'María Córdoba','maria.cordoba@example.com','$2b$12$ZD93kFaclofAWVgKGrFLm.YACfDTh3V6tuqIJqY.JpQffIl1In.uS','3108887766','Istmina, Chocó','artesano','2025-11-05 03:29:00',1),(3,'José Palacios','jose.palacios@example.com','$2b$12$ZD93kFaclofAWVgKGrFLm.YACfDTh3V6tuqIJqY.JpQffIl1In.uS','3209994433','Bahía Solano, Chocó','artesano','2025-11-05 03:29:00',1),(4,'Camila Rentería','camila.renteria@example.com','$2b$12$ZD93kFaclofAWVgKGrFLm.YACfDTh3V6tuqIJqY.JpQffIl1In.uS','3112223344','Quibdó, Chocó','cliente','2025-11-05 03:29:00',1),(5,'Administrador','admin@artesaniaschoco.com','$2b$12$ZD93kFaclofAWVgKGrFLm.YACfDTh3V6tuqIJqY.JpQffIl1In.uS','0000000000','Sistema Central','admin','2025-11-05 03:29:00',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-15  2:04:08
