# models.py

class Paciente:
    def __init__(self,
                id_paciente=None,
                dni=None,
                nombres=None,
                apellido_paterno=None,
                apellido_materno=None,
                fecha_nacimiento=None,
                estado_civil=None,
                profesion=None,
                calle=None,
                numero=None,
                distrito=None,
                provincia=None,
                num_hijos=None,
                observaciones=None
                ):

        self.id_paciente = id_paciente
        self.dni = dni
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.fecha_nacimiento = fecha_nacimiento
        self.estado_civil = estado_civil
        self.profesion = profesion
        self.calle = calle
        self.numero = numero
        self.distrito = distrito
        self.provincia = provincia
        self.num_hijos = num_hijos
        self.observaciones = observaciones

    def __repr__(self):
        return (
            f"Paciente(id_paciente={self.id_paciente}, dni='{self.dni}', "
            f"nombres='{self.nombres}', apellido_paterno='{self.apellido_paterno}', "
            f"apellido_materno='{self.apellido_materno}', fecha_nacimiento={self.fecha_nacimiento}, "
            f"estado_civil='{self.estado_civil}', profesion='{self.profesion}', "
            f"calle='{self.calle}', numero='{self.numero}', distrito='{self.distrito}', "
            f"provincia='{self.provincia}', num_hijos={self.num_hijos}, "
            f"observaciones='{self.observaciones}')"
        )


class Factura:
    def __init__(self, id_factura=None, fecha=None, estado_pago=None,
                 forma_financiamiento=None, monto_total=0.0, id_paciente=None):
        self.id_factura = id_factura
        self.fecha = fecha
        self.estado_pago = estado_pago
        self.forma_financiamiento = forma_financiamiento
        self.monto_total = monto_total
        self.id_paciente = id_paciente


class FichaMedica:
    def __init__(self, id_ficha=None, fecha_registro=None, marcha=None,
                 otros_aspectos=None, observaciones_medicas=None,
                 id_paciente=None, id_ingreso=None):

        self.id_ficha = id_ficha
        self.fecha_registro = fecha_registro
        self.marcha = marcha
        self.otros_aspectos = otros_aspectos
        self.observaciones_medicas = observaciones_medicas
        self.id_paciente = id_paciente
        self.id_ingreso = id_ingreso

    def __repr__(self):
        return (
            f"FichaMedica(id_ficha={self.id_ficha}, fecha_registro='{self.fecha_registro}', "
            f"marcha='{self.marcha}', otros_aspectos='{self.otros_aspectos}', "
            f"observaciones_medicas='{self.observaciones_medicas}', id_paciente={self.id_paciente}, "
            f"id_ingreso={self.id_ingreso})"
        )

class Enfermedad:
    def __init__(self, id_enfermedad=None, nombre=None, descripcion=None):
        self.id_enfermedad = id_enfermedad
        self.nombre = nombre
        self.descripcion = descripcion

    def __repr__(self):
        return (
            f"Enfermedad(id_enfermedad={self.id_enfermedad}, "
            f"nombre='{self.nombre}', descripcion='{self.descripcion}')"
        )

class Habitacion:
    def __init__(self,
                 id_habitacion=None,
                 num_habitacion=None,
                 estado=None,
                 tipo_habitacion=None):
        self.id_habitacion = id_habitacion
        self.num_habitacion = num_habitacion
        self.estado = estado
        self.tipo_habitacion = tipo_habitacion

    def __repr__(self):
        return (
            f"Habitacion(id={self.id_habitacion}, num='{self.num_habitacion}', "
            f"estado='{self.estado}', tipo='{self.tipo_habitacion}')"
        )

class Ingreso:
    def __init__(self,
                 id_ingreso=None,
                 fecha_ingreso=None,
                 id_paciente=None,
                 id_habitacion=None,
                 id_plan=None):
        self.id_ingreso = id_ingreso
        self.fecha_ingreso = fecha_ingreso
        self.id_paciente = id_paciente
        self.id_habitacion = id_habitacion
        self.id_plan = id_plan

    def __repr__(self):
        return (
            f"Ingreso(id={self.id_ingreso}, fecha='{self.fecha_ingreso}', "
            f"paciente={self.id_paciente}, habitacion={self.id_habitacion}, plan={self.id_plan})"
        )
