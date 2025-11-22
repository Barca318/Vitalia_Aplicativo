# dao.py
from db import get_connection
from models import Paciente, Factura, FichaMedica, Enfermedad, Habitacion, Ingreso

# ===================================================
# PACIENTE
# ===================================================
def insertar_paciente(p: Paciente):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cs = conn.cursor()

        cs.callproc('sp_insert_paciente', [
            p.dni,
            p.nombres,
            p.apellido_paterno,
            p.apellido_materno,
            p.fecha_nacimiento,
            p.estado_civil,
            p.profesion,
            p.calle,
            p.numero,
            p.distrito,
            p.provincia,
            p.num_hijos,
            p.observaciones
        ])

        cs.close()
        return True, "Insertado"

    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def actualizar_paciente(p: Paciente):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cs = conn.cursor()

        cs.callproc('sp_update_paciente', [
            p.id_paciente,
            p.dni,
            p.nombres,
            p.apellido_paterno,
            p.apellido_materno,
            p.fecha_nacimiento,
            p.estado_civil,
            p.profesion,
            p.calle,
            p.numero,
            p.distrito,
            p.provincia,
            p.num_hijos,
            p.observaciones
        ])

        cs.close()
        return True, "Actualizado"

    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def eliminar_paciente(id_paciente: int):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cs = conn.cursor()
        cs.callproc('sp_delete_paciente', [id_paciente])
        cs.close()
        return True, "Eliminado"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def listar_pacientes():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT
                id_paciente,
                dni,
                nombres,
                apellido_paterno,
                apellido_materno,
                fecha_nacimiento,
                estado_civil,
                profesion,
                calle,
                numero,
                distrito,
                provincia,
                num_hijos,
                observaciones
            FROM PACIENTE
        """)

        rows = cur.fetchall()
        cur.close()

        return [Paciente(**r) for r in rows]

    except Exception as e:
        print("Error listar_pacientes:", e)
        return []
    finally:
        conn.close()

# ===================================================
# FACTURA
# ===================================================
def registrar_factura(f: Factura):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cur = conn.cursor()
        # Insert directo (o puedes crear un sp)
        sql = "INSERT INTO FACTURA (fecha, estado_pago, forma_financiamiento, monto_total, id_paciente) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(sql, (f.fecha, f.estado_pago, f.forma_financiamiento, f.monto_total, f.id_paciente))
        cur.close()
        return True, "Factura registrada"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def buscar_factura_por_id(id_factura: int):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM FACTURA WHERE id_factura = %s", (id_factura,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Factura(**row)
        return None
    except Exception as e:
        print("Error buscar_factura_por_id:", e)
        return None
    finally:
        conn.close()

def actualizar_estado_pago(id_factura: int, nuevo_estado: str):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cur = conn.cursor()
        cur.execute("UPDATE FACTURA SET estado_pago = %s WHERE id_factura = %s", (nuevo_estado, id_factura))
        cur.close()
        return True, "Estado actualizado"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()


def listar_facturas_con_pacientes():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        query = """
            SELECT 
                f.id_factura,
                f.fecha,
                f.estado_pago,
                f.forma_financiamiento,
                f.monto_total,
                f.id_paciente,
                CONCAT(p.nombres, ' ', p.apellido_paterno, ' ', p.apellido_materno) AS paciente
            FROM FACTURA f
            INNER JOIN PACIENTE p ON f.id_paciente = p.id_paciente;
        """
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        print("Error listar_facturas_con_paciente:", e)
        return []
    finally:
        conn.close()

def total_facturado_general():
    conn = get_connection()
    if not conn:
        return 0.0
    try:
        cur = conn.cursor()
        cur.execute("SELECT IFNULL(SUM(monto_total),0) AS total FROM FACTURA")
        r = cur.fetchone()
        cur.close()
        return float(r[0]) if r else 0.0
    except Exception as e:
        print("Error total:", e)
        return 0.0
    finally:
        conn.close()

def total_facturado_por_paciente(id_paciente: int):
    conn = get_connection()
    if not conn:
        return 0.0
    try:
        cur = conn.cursor()
        cur.execute("SELECT IFNULL(SUM(monto_total),0) AS total FROM FACTURA WHERE id_paciente = %s", (id_paciente,))
        r = cur.fetchone()
        cur.close()
        return float(r[0]) if r else 0.0
    except Exception as e:
        print("Error total por paciente:", e)
        return 0.0
    finally:
        conn.close()
        
# ===================================================
# FICHA MEDICA
# ===================================================

def insertar_ficha_medica(fecha, marcha, otros, observ, id_paciente, id_ingreso):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO ficha_medica
            (fecha_registro, marcha, otros_aspectos, observaciones_medicas, id_paciente, id_ingreso)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fecha, marcha, otros, observ, id_paciente, id_ingreso))
        conn.commit()
        return True

    except Exception as e:
        print("Error insertar ficha médica:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def listar_fichas_por_paciente(id_paciente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT * FROM ficha_medica
            WHERE id_paciente = %s
        """
        cursor.execute(query, (id_paciente,))
        return cursor.fetchall()

    except Exception as e:
        print("Error listar fichas:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_ficha(id_ficha):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM ficha_medica WHERE id_ficha = %s"
        cursor.execute(query, (id_ficha,))
        return cursor.fetchone()

    except Exception as e:
        print("Error obtener ficha:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def actualizar_ficha(id_ficha, marcha, otros, observ):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE ficha_medica
            SET marcha=%s, otros_aspectos=%s, observaciones_medicas=%s
            WHERE id_ficha = %s
        """
        cursor.execute(query, (marcha, otros, observ, id_ficha))
        conn.commit()
        return True

    except Exception as e:
        print("Error actualizar ficha:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def eliminar_ficha(id_ficha):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM contiene WHERE id_ficha=%s", (id_ficha,))
        cursor.execute("DELETE FROM ficha_medica WHERE id_ficha=%s", (id_ficha,))
        conn.commit()
        return True

    except Exception as e:
        print("Error eliminar ficha:", e)
        return False
    finally:
        cursor.close()
        conn.close()



# ======================================
# TABLA CONTIENE — ENFERMEDADES
# ======================================

def insertar_enfermedad_en_ficha(id_ficha, id_enfermedad, tratamiento):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO contiene (id_ficha, id_enfermedad, tratamiento)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_ficha, id_enfermedad, tratamiento))
        conn.commit()
        return True

    except Exception as e:
        print("Error insertar enfermedad en ficha:", e)
        return False
    finally:
        cursor.close()
        conn.close()


def obtener_enfermedades_de_ficha(id_ficha):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT e.nombre, e.descripcion, c.tratamiento
            FROM contiene c
            INNER JOIN enfermedad e ON c.id_enfermedad = e.id_enfermedad
            WHERE c.id_ficha = %s
        """
        cursor.execute(query, (id_ficha,))
        return cursor.fetchall()

    except Exception as e:
        print("Error obtener enfermedades:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def eliminar_enfermedad_de_ficha(id_ficha, id_enfermedad):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM contiene WHERE id_ficha=%s AND id_enfermedad=%s",
            (id_ficha, id_enfermedad)
        )
        conn.commit()
        return True

    except Exception as e:
        print("Error eliminar enfermedad:", e)
        return False
    finally:
        cursor.close()
        conn.close()
        
from models import Habitacion, Ingreso
from db import get_connection

# ===================================================
# HABITACIONES
# ===================================================

def insertar_habitacion(h: Habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """INSERT INTO habitacion (num_habitacion, estado, tipo_habitacion)
                 VALUES (%s,%s,%s)"""
        cur.execute(sql, (h.num_habitacion, h.estado, h.tipo_habitacion))

        conn.commit()
        return True
    except Exception as e:
        print("Error insertar_habitacion:", e)
        return False
    finally:
        cur.close()
        conn.close()


def actualizar_habitacion(h: Habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor()

        sql = """UPDATE habitacion
                 SET num_habitacion=%s, estado=%s, tipo_habitacion=%s
                 WHERE id_habitacion=%s"""
        cur.execute(sql, (h.num_habitacion, h.estado, h.tipo_habitacion, h.id_habitacion))

        conn.commit()
        return True
    except Exception as e:
        print("Error actualizar_habitacion:", e)
        return False
    finally:
        cur.close()
        conn.close()


def eliminar_habitacion(id_habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # verificar ingresos activos
        cur.execute("""SELECT COUNT(*) FROM ingreso WHERE id_habitacion=%s""",
                    (id_habitacion,))
        (cant,) = cur.fetchone()

        if cant > 0:
            return False, "La habitación tiene ingresos activos"

        cur.execute("DELETE FROM habitacion WHERE id_habitacion=%s", (id_habitacion,))
        conn.commit()

        return True, "Eliminado"
    except Exception as e:
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def listar_habitaciones():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM habitacion")
        rows = cur.fetchall()

        return [Habitacion(**r) for r in rows]
    except:
        return []
    finally:
        cur.close()
        conn.close()


def buscar_habitaciones(num=None, tipo=None, estado=None):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM habitacion WHERE 1=1"
        params = []

        if num:
            sql += " AND num_habitacion LIKE %s"
            params.append(f"%{num}%")

        if tipo:
            sql += " AND tipo_habitacion = %s"
            params.append(tipo)

        if estado:
            sql += " AND estado = %s"
            params.append(estado)

        cur.execute(sql, params)
        return cur.fetchall()
    except Exception as e:
        print("Error buscar habitaciones:", e)
        return []
    finally:
        cur.close()
        conn.close()


def habitaciones_disponibles():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT * FROM habitacion WHERE estado='Disponible'")
        return cur.fetchall()
    except:
        return []
    finally:
        cur.close()
        conn.close()


def actualizar_estado_habitacion(id_habitacion, estado):
    """Cambiar estado: Disponible / Ocupada / Mantenimiento"""
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("UPDATE habitacion SET estado=%s WHERE id_habitacion=%s",
                    (estado, id_habitacion))
        conn.commit()
        return True
    except Exception as e:
        print("Error actualizar_estado_habitacion:", e)
        return False
    finally:
        cur.close()
        conn.close()

# ===================================================
# INGRESOS
# ===================================================

def registrar_ingreso(i: Ingreso):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # verificar habitación disponible
        cur.execute("SELECT estado FROM habitacion WHERE id_habitacion=%s",
                    (i.id_habitacion,))
        (estado,) = cur.fetchone()

        if estado != "Disponible":
            return False, "Habitación no disponible"

        # registrar ingreso
        sql = """INSERT INTO ingreso (fecha_ingreso, id_paciente, id_habitacion, id_plan)
                 VALUES (%s,%s,%s,%s)"""
        cur.execute(sql, (i.fecha_ingreso, i.id_paciente, i.id_habitacion, i.id_plan))

        # ocupar habitación
        cur.execute("""UPDATE habitacion SET estado='Ocupada'
                       WHERE id_habitacion=%s""", (i.id_habitacion,))

        conn.commit()
        return True, "Ingreso registrado"

    except Exception as e:
        print("Error registrar_ingreso:", e)
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def editar_ingreso(i: Ingreso, habitacion_anterior):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # si cambia la habitación
        if i.id_habitacion != habitacion_anterior:
            cur.execute("UPDATE habitacion SET estado='Disponible' WHERE id_habitacion=%s",
                        (habitacion_anterior,))
            cur.execute("UPDATE habitacion SET estado='Ocupada' WHERE id_habitacion=%s",
                        (i.id_habitacion,))

        sql = """UPDATE ingreso
                 SET fecha_ingreso=%s, id_paciente=%s,
                     id_habitacion=%s, id_plan=%s
                 WHERE id_ingreso=%s"""

        cur.execute(sql, (i.fecha_ingreso, i.id_paciente,
                          i.id_habitacion, i.id_plan, i.id_ingreso))

        conn.commit()
        return True, "Ingreso actualizado"

    except Exception as e:
        print("Error editar_ingreso:", e)
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def eliminar_ingreso(id_ingreso, id_habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM ingreso WHERE id_ingreso=%s", (id_ingreso,))

        # liberar la habitación
        cur.execute("UPDATE habitacion SET estado='Disponible' WHERE id_habitacion=%s",
                    (id_habitacion,))

        conn.commit()
        return True, "Ingreso eliminado"

    except Exception as e:
        print("Error eliminar_ingreso:", e)
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def listar_ingresos():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        query = """
            SELECT i.id_ingreso, i.fecha_ingreso,
                   CONCAT(p.nombres, ' ', p.apellido_paterno) AS paciente,
                   h.num_habitacion AS habitacion,
                   i.id_plan
            FROM ingreso i
            INNER JOIN paciente p ON p.id_paciente = i.id_paciente
            INNER JOIN habitacion h ON h.id_habitacion = i.id_habitacion
        """

        cur.execute(query)
        return cur.fetchall()
    except:
        return []
    finally:
        cur.close()
        conn.close()


def historial_habitacion(id_habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM ingreso
            WHERE id_habitacion = %s
            ORDER BY fecha_ingreso
        """, (id_habitacion,))

        return cur.fetchall()

    except:
        return []
    finally:
        cur.close()
        conn.close()
