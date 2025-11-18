USE vitalia_db;

-- insertar

DELIMITER //
CREATE PROCEDURE sp_insert_paciente(
    IN p_dni CHAR(8),
    IN p_nombres VARCHAR(100),
    IN p_apellido_paterno VARCHAR(100),
    IN p_apellido_materno VARCHAR(100),
    IN p_fecha_nacimiento DATE
)
BEGIN
    INSERT INTO PACIENTE(dni, nombres, apellido_paterno, apellido_materno, fecha_nacimiento)
    VALUES(p_dni, p_nombres, p_apellido_paterno, p_apellido_materno, p_fecha_nacimiento);
END //
DELIMITER ;

-- actualizar

DELIMITER $$

CREATE PROCEDURE sp_update_paciente (
    IN p_id INT,
    IN p_dni VARCHAR(15),
    IN p_nombres VARCHAR(100),
    IN p_ap_paterno VARCHAR(100),
    IN p_ap_materno VARCHAR(100),
    IN p_fecha_nac DATE
)
BEGIN
    UPDATE paciente
    SET 
        dni = p_dni,
        nombres = p_nombres,
        apellido_paterno = p_ap_paterno,
        apellido_materno = p_ap_materno,
        fecha_nacimiento = p_fecha_nac
    WHERE id_paciente = p_id;
END $$

DELIMITER ;

-- eliminar

DELIMITER //
CREATE PROCEDURE sp_delete_paciente(
    IN p_id INT
)
BEGIN
    DELETE FROM PACIENTE WHERE id_paciente = p_id;
END //
DELIMITER ;


CREATE TABLE LOG_PACIENTE(
   id INT AUTO_INCREMENT PRIMARY KEY,
   mensaje VARCHAR(255),
   fecha DATETIME
);

DELIMITER //
CREATE TRIGGER trg_paciente_insert
AFTER INSERT ON PACIENTE
FOR EACH ROW
BEGIN
   INSERT INTO LOG_PACIENTE(mensaje, fecha)
   VALUES(CONCAT('Se insertó el paciente ', NEW.nombres), NOW());
END//
DELIMITER ;





