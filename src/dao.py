# dao.py
from db import get_connection
from models import Paciente, Factura, FichaMedica, Enfermedad, Habitacion, Ingreso


# ---------- PACIENTE ----------
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


# ---------- FACTURA ----------
def registrar_factura(f: Factura):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"
    try:
        cur = conn.cursor()
        
        sql = "INSERT INTO FACTURA (fecha, estado_pago, forma_financiamiento, monto_total, id_paciente) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(sql, (f.fecha, f.estado_pago, f.forma_financiamiento, f.monto_total, f.id_paciente))
        cur.close()
        return True, "Factura registrada"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def cargar_datos_paciente_factura(self):
    try:
        id_pac = int(self.ent_f_id_pac.get())
    except:
        messagebox.showerror("Error", "ID Paciente inválido.")
        return

    pac = dao.obtener_paciente_por_id(id_pac)
    if not pac:
        messagebox.showerror("Error", "No existe un paciente con ese ID.")
        return

    # Cargar datos
    self.lbl_f_pac_nombre.config(text=f"{pac.nombres} {pac.apellido_paterno} {pac.apellido_materno}")
    self.lbl_f_pac_dni.config(text=pac.dni)




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
def eliminar_factura(id_factura: int):
    conn = get_connection()
    if not conn:
        return False, "No hay conexión"

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM FACTURA WHERE id_factura = %s", (id_factura,))
        conn.commit()
        cur.close()
        return True, "Factura eliminada"

    except Exception as e:
        return False, str(e)

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



def listar_promociones():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM promocion")
        return cur.fetchall()
    except Exception as e:
        print("Error listar_promociones:", e)
        return []
    finally:
        cur.close()
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

def listar_todas_fichas():
    sql = """
        SELECT 
            f.id_ficha,
            f.id_paciente,
            p.nombres,
            p.apellido_paterno,
            f.fecha_registro,
            f.marcha,
            f.otros_aspectos,
            f.observaciones_medicas,
            f.id_ingreso
        FROM ficha_medica f
        JOIN paciente p ON p.id_paciente = f.id_paciente
        ORDER BY f.id_ficha
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data



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

def listar_todas_enfermedades():
    sql = """
        SELECT 
            f.id_ficha,
            p.nombres,
            p.apellido_paterno,
            e.nombre,
            c.tratamiento
        FROM contiene c
        JOIN ficha_medica f ON f.id_ficha = c.id_ficha
        JOIN paciente p ON p.id_paciente = f.id_paciente
        JOIN enfermedad e ON e.id_enfermedad = c.id_enfermedad
        ORDER BY f.id_ficha, e.nombre;
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data


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


def buscar_habitacion(num_habitacion, estado, tipo_habitacion):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        sql = "SELECT * FROM habitacion WHERE 1=1"
        params = []

        if num_habitacion:
            sql += " AND num_habitacion LIKE %s"
            params.append(f"%{num_habitacion}%")

        if tipo_habitacion:
            sql += " AND tipo_habitacion = %s"
            params.append(tipo_habitacion)

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

        cur.execute("SELECT estado FROM habitacion WHERE id_habitacion=%s",
                    (i.id_habitacion,))
        (estado,) = cur.fetchone()

        if estado != "Disponible":
            return False, "La habitación no está disponible"

        sql = """INSERT INTO ingreso (fecha_ingreso, id_paciente, id_habitacion, id_plan)
                 VALUES (%s,%s,%s,%s)"""
        cur.execute(sql, (i.fecha_ingreso, i.id_paciente, i.id_habitacion, i.id_plan))

        cur.execute("UPDATE habitacion SET estado='Ocupada' WHERE id_habitacion=%s",
                    (i.id_habitacion,))

        conn.commit()
        return True, "Ingreso registrado correctamente"

    except Exception as e:
        print("Error registrar_ingreso:", e)
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def editar_ingreso(i: Ingreso, hab_anterior):
    try:
        conn = get_connection()
        cur = conn.cursor()

        if i.id_habitacion != hab_anterior:
            cur.execute("UPDATE habitacion SET estado='Disponible' WHERE id_habitacion=%s",
                        (hab_anterior,))
            cur.execute("UPDATE habitacion SET estado='Ocupada' WHERE id_habitacion=%s",
                        (i.id_habitacion,))

        sql = """UPDATE ingreso
                 SET fecha_ingreso=%s, id_paciente=%s,
                     id_habitacion=%s, id_plan=%s
                 WHERE id_ingreso=%s"""
        cur.execute(sql, (i.fecha_ingreso, i.id_paciente, i.id_habitacion, 
                          i.id_plan, i.id_ingreso))

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

        sql = """
            SELECT i.id_ingreso, i.fecha_ingreso,
                   CONCAT(p.nombres,' ',p.apellido_paterno,' ',p.apellido_materno) AS paciente,
                   h.num_habitacion AS habitacion,
                   i.id_plan,
                   i.id_paciente,
                   i.id_habitacion
            FROM ingreso i
            INNER JOIN paciente p ON p.id_paciente=i.id_paciente
            INNER JOIN habitacion h ON h.id_habitacion=i.id_habitacion
        """
        cur.execute(sql)
        return cur.fetchall()

    except Exception as e:
        print("Error listar_ingresos:", e)
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
            WHERE id_habitacion=%s
            ORDER BY fecha_ingreso
        """, (id_habitacion,))

        return cur.fetchall()

    except:
        return []
    finally:
        cur.close()
        conn.close()
        
def listar_planes():
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM plan_servicio")
        return cur.fetchall()
    except:
        return []
    finally:
        cur.close()
        conn.close()


def obtener_plan(id_plan):
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM plan_servicio WHERE id_plan=%s", (id_plan,))
        return cur.fetchone()
    except Exception as e:
        print("Error obtener_plan:", e)
        return None
    finally:
        cur.close()
        conn.close()

def registrar_factura_plan(id_paciente, id_plan):
    try:
        plan = obtener_plan(id_plan)
        if not plan:
            return False, "El plan no existe"

        monto = plan["tarifa"]

        conn = get_connection()
        cur = conn.cursor()

        sql = """INSERT INTO factura 
                 (id_paciente, fecha, estado_pago, forma_financiamiento, monto_total, id_plan)
                 VALUES (%s, NOW(), 'Pendiente', 'Plan de servicio', %s, %s)"""

        cur.execute(sql, (id_paciente, monto, id_plan))
        conn.commit()

        return True, "Factura generada correctamente"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        cur.close()
        conn.close()

        
def obtener_datos_completos_paciente(id_paciente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Datos del paciente
        cursor.execute("SELECT * FROM paciente WHERE id_paciente=%s", (id_paciente,))
        paciente = cursor.fetchone()

        # Facturas
        cursor.execute("SELECT * FROM factura WHERE id_paciente=%s", (id_paciente,))
        facturas = cursor.fetchall()

        # Fichas médicas
        cursor.execute("""
            SELECT * FROM ficha_medica 
            WHERE id_paciente=%s
        """, (id_paciente,))
        fichas = cursor.fetchall()

        # Enfermedades según ficha
        cursor.execute("""
            SELECT c.id_ficha, e.nombre, c.tratamiento
            FROM contiene c
            JOIN enfermedad e ON c.id_enfermedad = e.id_enfermedad
            JOIN ficha_medica f ON f.id_ficha = c.id_ficha
            WHERE f.id_paciente=%s
        """, (id_paciente,))
        enfermedades = cursor.fetchall()

        # Ingresos
        cursor.execute("""
            SELECT * FROM ingreso WHERE id_paciente=%s
        """, (id_paciente,))
        ingresos = cursor.fetchall()

        return paciente, facturas, fichas, enfermedades, ingresos

    except Exception as e:
        print("Error obtener datos completos:", e)
        return None, [], [], [], []
    finally:
        cursor.close()
        conn.close()
def obtener_paciente_por_id(id_paciente: int):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM PACIENTE WHERE id_paciente = %s", (id_paciente,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Paciente(**row)
        return None
    except Exception as e:
        print("Error obtener_paciente_por_id:", e)
        return None
    finally:
        conn.close()

        
