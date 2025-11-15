DROP FUNCTION IF EXISTS fn_total_facturas_paciente;
DELIMITER //
CREATE FUNCTION fn_total_facturas_paciente(p_id INT)
	RETURNS DECIMAL(12,2)
    DETERMINISTIC
BEGIN
	DECLARE total DECIMAL(12,2);
    SELECT SUM(monto_total) INTO TOTAL
    FROM FACTURA
    WHERE id_paciente = p_id;
    RETURN IFNULL(total, 0);
END //
DELIMITER ;
