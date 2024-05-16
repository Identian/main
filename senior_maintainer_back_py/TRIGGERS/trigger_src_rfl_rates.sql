DELIMITER $$
CREATE TRIGGER src_rfl_rates_delete_restrictions 
BEFORE DELETE ON precia_sources.src_rfl_rates
FOR EACH ROW 
BEGIN 
	IF OLD.rate_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden eliminar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER src_rfl_rates_update_restrictions 
BEFORE UPDATE ON precia_sources.src_rfl_rates
FOR EACH ROW 
BEGIN 
	IF OLD.rate_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden actualizar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER src_rfl_rates_insert_restrictions 
BEFORE INSERT ON precia_sources.src_rfl_rates
FOR EACH ROW 
BEGIN 
	IF NEW.rate_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden insertar registros anteriores a el día de hoy.';
	END IF;
END;
END $$