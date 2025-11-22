-- Paciente
DELIMITER //
CREATE PROCEDURE sp_insert_paciente(
    IN p_dni CHAR(8),
    IN p_nombres VARCHAR(100),
    IN p_apellido_paterno VARCHAR(100),
    IN p_apellido_materno VARCHAR(100),
    IN p_fecha_nacimiento DATE,
    IN p_estado_civil VARCHAR(30),
    IN p_profesion VARCHAR(80),
    IN p_calle VARCHAR(120),
    IN p_numero VARCHAR(15),
    IN p_distrito VARCHAR(80),
    IN p_provincia VARCHAR(80),
    IN p_num_hijos INT,
    IN p_observaciones VARCHAR(500)
)
BEGIN
    INSERT INTO paciente (
        dni, nombres, apellido_paterno, apellido_materno, fecha_nacimiento,
        estado_civil, profesion, calle, numero, distrito, provincia,
        num_hijos, observaciones
    ) VALUES (
        p_dni, p_nombres, p_apellido_paterno, p_apellido_materno, p_fecha_nacimiento,
        p_estado_civil, p_profesion, p_calle, p_numero, p_distrito, p_provincia,
        p_num_hijos, p_observaciones
    );
END //
DELIMITER ;


DELIMITER $$

CREATE PROCEDURE sp_update_paciente (
    IN p_id INT,
    IN p_dni CHAR(8),
    IN p_nombres VARCHAR(100),
    IN p_apellido_paterno VARCHAR(100),
    IN p_apellido_materno VARCHAR(100),
    IN p_fecha_nacimiento DATE,
    IN p_estado_civil VARCHAR(30),
    IN p_profesion VARCHAR(80),
    IN p_calle VARCHAR(120),
    IN p_numero VARCHAR(15),
    IN p_distrito VARCHAR(80),
    IN p_provincia VARCHAR(80),
    IN p_num_hijos INT,
    IN p_observaciones VARCHAR(500)
)
BEGIN
    UPDATE paciente
    SET 
        dni = p_dni,
        nombres = p_nombres,
        apellido_paterno = p_apellido_paterno,
        apellido_materno = p_apellido_materno,
        fecha_nacimiento = p_fecha_nacimiento,
        estado_civil = p_estado_civil,
        profesion = p_profesion,
        calle = p_calle,
        numero = p_numero,
        distrito = p_distrito,
        provincia = p_provincia,
        num_hijos = p_num_hijos,
        observaciones = p_observaciones
    WHERE id_paciente = p_id;
END $$

DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_delete_paciente(
    IN p_id INT
)
BEGIN
    DELETE FROM paciente WHERE id_paciente = p_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_listar_pacientes()
BEGIN
    SELECT 
        id_paciente, dni, nombres, apellido_paterno, apellido_materno,
        fecha_nacimiento, estado_civil, profesion, calle, numero,
        distrito, provincia, num_hijos, observaciones
    FROM paciente;
END //
DELIMITER ;


-- Factura

DELIMITER //
CREATE PROCEDURE sp_insert_factura(
    IN p_fecha DATE,
    IN p_estado_pago VARCHAR(30),
    IN p_forma_financiamiento VARCHAR(40),
    IN p_monto_total DECIMAL(12,2),
    IN p_id_paciente INT
)
BEGIN
    INSERT INTO factura (
        fecha, estado_pago, forma_financiamiento, monto_total, id_paciente
    ) VALUES (
        p_fecha, p_estado_pago, p_forma_financiamiento, p_monto_total, p_id_paciente
    );
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_delete_factura(
    IN p_id_factura INT
)
BEGIN
    DELETE FROM factura WHERE id_factura = p_id_factura;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_listar_facturas()
BEGIN
    SELECT 
        id_factura, fecha, estado_pago,
        forma_financiamiento, monto_total, id_paciente
    FROM factura;
END //
DELIMITER ;


