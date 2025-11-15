-- Insertar Paciente

DROP PROCEDURE IF EXISTS sp_paciente_insert;
DELIMITER //
CREATE PROCEDURE sp_paciente_insert(
	IN p_dni CHAR(8),
    IN p_nombres VARCHAR(100),
    IN p_ap_pat VARCHAR(100),
    IN p_ap_mat VARCHAR(100),
    IN p_estado_civil VARCHAR(30)
)
BEGIN
INSERT INTO PACIENTE(dni,nombres,apellido_paterno, apellido_materno, estado_civil) VALUES
	(p_dni,p_nombres,p_ap_pat, p_ap_mat, p_estado_civil);
	SELECT 'Paciente insertado correctamente' AS mensaje;
END //
DELIMITER ;

-- Actualizar Paciente

DROP PROCEDURE IF EXISTS sp_paciente_update;
DELIMITER //
CREATE PROCEDURE sp_paciente_update(
	IN p_id INT,
	IN p_dni CHAR(8),
    IN p_nombres VARCHAR(100),
    IN p_ap_pat VARCHAR(100),
    IN p_ap_mat VARCHAR(100),
    IN p_estado_civil VARCHAR(30)
)
BEGIN
UPDATE PACIENTE
	SET Nombres = p_nombres,
    apellido_paterno = p_ap_pat, 
    apellido_materno = p_ap_mat, 
    estado_civil = p_estado_civil
	WHERE id_paciente = p_id;
	SELECT 'Paciente actualizado correctamente' AS mensaje;
END //
DELIMITER ;

-- Eliminar Paciente

DROP PROCEDURE IF EXISTS sp_paciente_delete;
DELIMITER //
CREATE PROCEDURE sp_paciente_delete(
	IN p_id INT)
BEGIN
	DELETE FROM PACIENTE WHERE id_paciente= p_id;
	SELECT 'Paciente eliminado correctamente' AS mensaje;
END //
DELIMITER ;

-- Registrar Factura

DROP PROCEDURE IF EXISTS sp_factura_insert;
DELIMITER //
CREATE PROCEDURE sp_factura_insert(
	IN p_fecha DATE,
    IN p_estado VARCHAR(30),
    IN p_monto DECIMAL(12,2),
    IN p_id_paciente INT
    )
BEGIN
	INSERT INTO FACTURA(fecha, estado_pago, monto_total, id_paciente) VALUES
		(p_fecha, p_estado, p_monto, p_id_paciente);
	SELECT 'Factura registrada correctamente' AS mensaje;
END //
DELIMITER ;







