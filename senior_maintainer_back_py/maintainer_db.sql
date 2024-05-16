CREATE TABLE IF NOT EXISTS `APPROVE_USER` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Identificador para cada campo de la tabla.',
  `FULL_NAME` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Nombre de la persona que está autorizada a aprobar.',
  `EMAIL` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Correo de la persona que está autorizada a aprobar.',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla que registra los usuarios autorizados para aprobar y para cada uno, su correo, a donde le llegaran las solicitudes de aprobación.';

CREATE TABLE IF NOT EXISTS `DATABASE_MAINTAINER` (
  `ID` int NOT NULL AUTO_INCREMENT COMMENT 'Identificador para cada nombre de base de datos.',
  `DATABASE_NAME` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Campo que guarda el nombre de una base de datos en la cual se pueden realizar transacciones usando el mantenedor.',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `DATABASE_NAME` (`DATABASE_NAME`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla que registra los nombres de los esquemas disponibles para la solución.';


CREATE TABLE IF NOT EXISTS `MAINTAINER_REQUEST` (
  `REQUEST_QUERY` varchar(4096) NOT NULL COMMENT 'Query que se solicita ejecutar.',
  `DATABASE_NAME` varchar(32) NOT NULL COMMENT 'Base de datos donde se ejecutara el Query.',
  `RECORDS_TO_AFFECT` decimal(8,0) NOT NULL COMMENT 'Numero de registros a afectar.',
  `REQUESTER_EMAIL` varchar(32) NOT NULL COMMENT 'Correo del solicitante.',
  `APPROVER_EMAIL` varchar(32) NOT NULL COMMENT 'Correo de la persona a aprobar.',
  `REQUEST_DATETIME` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de la solicitud.',
  `REQUEST_ID` varchar(26) NOT NULL COMMENT 'Identificador que permite identificar una transacción por medio de un dato de menor tamaño a el hash.',
  `REQUEST_PROCESS_DATETIME` datetime DEFAULT NULL COMMENT 'Fecha de aprobación.',
  `REQUEST_STATUS` varchar(16) NOT NULL DEFAULT 'SOLICITADO' COMMENT 'Estado de la solicitud.',
  `REQUEST_HASH_KEY` varchar(512) NOT NULL COMMENT 'Llave de la solicitud.',
  `REQUEST_MESSAGE` varchar(4096) NOT NULL COMMENT 'Mensaje final de la solicitud.',
  `REQUEST_DESCRIPTION` varchar(1024) NOT NULL COMMENT 'Información de la solicitud que se realiza.',
  `REQUEST_INTDATE` int NOT NULL COMMENT 'Fecha en la que se realiza la solicitud pero escrita en un numero que describe la fecha. Por ejemplo: 2023/03/16 se veria como 20230316.',
  PRIMARY KEY (`REQUEST_INTDATE`,`REQUEST_HASH_KEY`) USING BTREE,
  CONSTRAINT `CHK_REQUEST_STATUS` CHECK ((`REQUEST_STATUS` in (_utf8mb4'SOLICITADO',_utf8mb4'APROBADO',_utf8mb4'RECHAZADO',_utf8mb4'ERROR')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Tabla que registra todas las solicitudes que llegan por medio del mantenedor.'
PARTITION BY HASH (`REQUEST_INTDATE`)
PARTITIONS 4;

DELETE FROM `APPROVE_USER`;
INSERT INTO `APPROVE_USER` (`ID`, `FULL_NAME`, `EMAIL`) VALUES
	(1, 'Diego Dussan', 'ddussan@precia.co');