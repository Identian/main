DELIMITER $$
CREATE TRIGGER prc_rfl_operations_delete_restrictions 
BEFORE DELETE ON precia_process.prc_rfl_operations
FOR EACH ROW 
BEGIN 
	IF OLD.operation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden eliminar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER prc_rfl_operations_update_restrictions 
BEFORE UPDATE ON precia_process.prc_rfl_operations
FOR EACH ROW 
BEGIN 
	IF OLD.operation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden actualizar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER prc_rfl_operations_insert_restrictions 
BEFORE INSERT ON precia_process.prc_rfl_operations
FOR EACH ROW 
BEGIN 
	IF NEW.operation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden insertar registros anteriores a el día de hoy.';
	END IF;
END;
END $$