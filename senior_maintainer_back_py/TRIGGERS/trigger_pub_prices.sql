DELIMITER $$
CREATE TRIGGER pub_rfl_prices_delete_restrictions 
BEFORE DELETE ON precia_published.pub_rfl_prices 
FOR EACH ROW 
BEGIN 
	IF OLD.valuation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden eliminar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER pub_rfl_prices_update_restrictions 
BEFORE UPDATE ON precia_published.pub_rfl_prices 
FOR EACH ROW 
BEGIN 
	IF OLD.valuation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden actualizar registros anteriores a el día de hoy.';
	END IF;
END;
END $$
DELIMITER $$
CREATE TRIGGER pub_rfl_prices_insert_restrictions 
BEFORE INSERT ON precia_published.pub_rfl_prices 
FOR EACH ROW 
BEGIN 
	IF NEW.valuation_date < DATE(DATE_FORMAT(DATE_SUB(UTC_TIMESTAMP,INTERVAL 5 HOUR),"%Y-%m-%d")) THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se pueden insertar registros anteriores a el día de hoy.';
	END IF;
END;
END $$