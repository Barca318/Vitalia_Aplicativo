# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Paciente, Factura, FichaMedica, Enfermedad, Habitacion, Ingreso
from dao import insertar_enfermedad_a_paciente, listar_enfermedades_por_paciente, eliminar_enfermedad_de_paciente
import dao


class VitaliaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vitalia - Registro")
        self.geometry("1100x650")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        self.tab_pacientes = ttk.Frame(tab_control)
        self.tab_facturas = ttk.Frame(tab_control)
        self.tab_fichamedica = ttk.Frame(tab_control)
        self.tab_habitaciones = ttk.Frame(tab_control)
        self.tab_ingresos = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_pacientes, text='Pacientes')
        tab_control.add(self.tab_facturas, text='Facturas')
        tab_control.add(self.tab_fichamedica, text='Ficha Médica')
        tab_control.add(self.tab_habitaciones, text='Habitaciones')
        tab_control.add(self.tab_ingresos, text='Ingresos')
        
        tab_control.pack(expand=1, fill='both')

        self.build_pacientes_tab()
        self.build_facturas_tab()
        self.build_ficha_medica_tab()



    # ---------------- Pacientes ----------------
    def build_pacientes_tab(self):
        frame = self.tab_pacientes

        labels = [
            "DNI:", "Nombres:", "Apellido Paterno:", "Apellido Materno:",
            "Fecha Nac (YYYY-MM-DD):",
            "Estado Civil:", "Profesión:", "Calle:", "Número:",
            "Distrito:", "Provincia:", "Número de Hijos:", "Observaciones:"
        ]

        self.entries = []
        row = 0
        for label in labels:
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(frame, width=35)
            entry.grid(row=row, column=1, padx=5, pady=5)
            self.entries.append(entry)
            row += 1

        (self.ent_dni, self.ent_nombres, self.ent_ap_pat, self.ent_ap_mat,
        self.ent_fecha, self.ent_estado_civil, self.ent_profesion, self.ent_calle,
        self.ent_numero, self.ent_distrito, self.ent_provincia,
        self.ent_num_hijos, self.ent_observaciones) = self.entries

        ttk.Button(frame, text="Insertar", command=self.insertar_paciente).grid(row=row, column=0, pady=8)
        ttk.Button(frame, text="Actualizar (por ID)", command=self.actualizar_paciente).grid(row=row, column=1, pady=8)
        ttk.Button(frame, text="Eliminar (por ID)", command=self.eliminar_paciente).grid(row=row, column=2, pady=8)

        ttk.Label(frame, text="ID (actualizar/eliminar):").grid(row=0, column=2)
        self.ent_id_oper = ttk.Entry(frame, width=15)
        self.ent_id_oper.grid(row=0, column=3)

        row += 1

        self.tree_pacientes = ttk.Treeview(
            frame,
            columns=(
                'id','dni','nombres','apP','apM','fecha',
                'estado','prof','calle','num','dist','prov','hijos','obs'
            ),
            show='headings',
            height=12
        )

        headers = [
            ('id', 'ID'), ('dni', 'DNI'), ('nombres', 'Nombres'),
            ('apP','A. Paterno'), ('apM','A. Materno'),
            ('fecha','Fecha Nac'), ('estado',"Estado Civil"),
            ('prof','Profesión'), ('calle','Calle'), ('num',"Número"),
            ('dist',"Distrito"), ('prov',"Provincia"),
            ('hijos',"Hijos"), ('obs',"Observaciones")
        ]

        for col, text in headers:
            self.tree_pacientes.heading(col, text=text)
            self.tree_pacientes.column(col, width=100)

        self.tree_pacientes.grid(row=row, column=0, columnspan=4, sticky='nsew', pady=8)
        frame.grid_rowconfigure(row, weight=1)

        ttk.Button(frame, text="Refrescar lista", command=self.refrescar_pacientes).grid(row=row+1, column=0, pady=5)

        self.refrescar_pacientes()
        

    # ---------------- FUNCIONES PACIENTE ----------------

    def insertar_paciente(self):
        try:
            p = Paciente(
                dni=self.ent_dni.get(),
                nombres=self.ent_nombres.get(),
                apellido_paterno=self.ent_ap_pat.get(),
                apellido_materno=self.ent_ap_mat.get(),
                fecha_nacimiento=self.ent_fecha.get(),
                estado_civil=self.ent_estado_civil.get(),
                profesion=self.ent_profesion.get(),
                calle=self.ent_calle.get(),
                numero=self.ent_numero.get(),
                distrito=self.ent_distrito.get(),
                provincia=self.ent_provincia.get(),
                num_hijos=int(self.ent_num_hijos.get() or 0),
                observaciones=self.ent_observaciones.get()
            )
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
            return

        ok, msg = dao.insertar_paciente(p)
        messagebox.showinfo("Insertar", msg if ok else f"Error: {msg}")
        self.refrescar_pacientes()

    def actualizar_paciente(self):
        idv = self.ent_id_oper.get()
        if not idv:
            messagebox.showwarning("Actualizar", "Debe indicar ID")
            return

        try:
            p = Paciente(
                id_paciente=int(idv),
                dni=self.ent_dni.get(),
                nombres=self.ent_nombres.get(),
                apellido_paterno=self.ent_ap_pat.get(),
                apellido_materno=self.ent_ap_mat.get(),
                fecha_nacimiento=self.ent_fecha.get(),
                estado_civil=self.ent_estado_civil.get(),
                profesion=self.ent_profesion.get(),
                calle=self.ent_calle.get(),
                numero=self.ent_numero.get(),
                distrito=self.ent_distrito.get(),
                provincia=self.ent_provincia.get(),
                num_hijos=int(self.ent_num_hijos.get() or 0),
                observaciones=self.ent_observaciones.get()
            )
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
            return

        ok,msg = dao.actualizar_paciente(p)
        messagebox.showinfo("Actualizar", msg if ok else f"Error: {msg}")
        self.refrescar_pacientes()

    def eliminar_paciente(self):
        idv = self.ent_id_oper.get()
        if not idv:
            messagebox.showwarning("Eliminar", "Debe indicar ID")
            return

        ok,msg = dao.eliminar_paciente(int(idv))
        messagebox.showinfo("Eliminar", msg if ok else f"Error: {msg}")
        self.refrescar_pacientes()

    def refrescar_pacientes(self):
        for row in self.tree_pacientes.get_children():
            self.tree_pacientes.delete(row)

        rows = dao.listar_pacientes()
        for p in rows:
            self.tree_pacientes.insert(
                '',
                'end',
                values=(
                    p.id_paciente, p.dni, p.nombres, p.apellido_paterno, p.apellido_materno,
                    p.fecha_nacimiento, p.estado_civil, p.profesion, p.calle, p.numero,
                    p.distrito, p.provincia, p.num_hijos, p.observaciones
                )
            )

    
    def ui_asignar_enfermedad(self):
        win = tk.Toplevel(self)
        win.title("Asignar Enfermedad a Paciente")

        tk.Label(win, text="ID Paciente:").grid(row=0, column=0, padx=5, pady=5)
        ent_id_p = tk.Entry(win)
        ent_id_p.grid(row=0, column=1)

        tk.Label(win, text="ID Enfermedad:").grid(row=1, column=0, padx=5, pady=5)
        ent_id_e = tk.Entry(win)
        ent_id_e.grid(row=1, column=1)

        def ejecutar():
            id_p = int(ent_id_p.get())
            id_e = int(ent_id_e.get())
            ok, msg = insertar_enfermedad_a_paciente(id_p, id_e)
            messagebox.showinfo("Resultado", msg)

        tk.Button(win, text="Asignar", command=ejecutar).grid(row=2, column=0, columnspan=2, pady=10)

    def ui_listar_enfermedades(self):
        win = tk.Toplevel(self)
        win.title("Enfermedades del Paciente")

        tk.Label(win, text="ID Paciente:").grid(row=0, column=0, padx=5, pady=5)
        ent_id_p = tk.Entry(win)
        ent_id_p.grid(row=0, column=1)

        txt = tk.Text(win, width=50, height=10)
        txt.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        def ejecutar():
            id_p = int(ent_id_p.get())
            datos = listar_enfermedades_por_paciente(id_p)
            txt.delete("1.0", tk.END)

            if not datos:
                txt.insert(tk.END, "No tiene enfermedades registradas.")
                return

            for e in datos:
                txt.insert(tk.END, f"{e['id_enfermedad']} - {e['nombre_enfermedad']}\n")

        tk.Button(win, text="Listar", command=ejecutar).grid(row=1, column=0, columnspan=2, pady=10)


    def ui_eliminar_enfermedad(self):
        win = tk.Toplevel(self)
        win.title("Eliminar Enfermedad del Paciente")

        tk.Label(win, text="ID Paciente:").grid(row=0, column=0, padx=5, pady=5)
        ent_id_p = tk.Entry(win)
        ent_id_p.grid(row=0, column=1)

        tk.Label(win, text="ID Enfermedad:").grid(row=1, column=0, padx=5, pady=5)
        ent_id_e = tk.Entry(win)
        ent_id_e.grid(row=1, column=1)

        def ejecutar():
            id_p = int(ent_id_p.get())
            id_e = int(ent_id_e.get())

            ok, msg = eliminar_enfermedad_de_paciente(id_p, id_e)
            messagebox.showinfo("Resultado", msg)

        tk.Button(win, text="Eliminar", command=ejecutar).grid(row=2, column=0, columnspan=2, pady=10)


    
    # ---------------- Facturas ----------------
    def build_facturas_tab(self):
        frame = self.tab_facturas

        ttk.Label(frame, text="ID Paciente:").grid(row=0, column=0, sticky='e')
        self.ent_f_id_pac = ttk.Entry(frame); self.ent_f_id_pac.grid(row=0,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
        self.ent_f_fecha = ttk.Entry(frame); self.ent_f_fecha.grid(row=1,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Estado pago:").grid(row=2, column=0, sticky='e')
        self.ent_f_estado = ttk.Entry(frame); self.ent_f_estado.grid(row=2,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Forma financiamiento:").grid(row=3, column=0, sticky='e')
        self.ent_f_forma = ttk.Entry(frame); self.ent_f_forma.grid(row=3,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Monto total:").grid(row=4, column=0, sticky='e')
        self.ent_f_monto = ttk.Entry(frame); self.ent_f_monto.grid(row=4,column=1,padx=5,pady=5)

        btn_reg = ttk.Button(frame, text="Registrar factura", command=self.registrar_factura)
        btn_reg.grid(row=5, column=0, pady=8)
        btn_total = ttk.Button(frame, text="Total general", command=self.mostrar_total_general)
        btn_total.grid(row=5, column=1, pady=8)
        btn_total_pac = ttk.Button(frame, text="Total por paciente", command=self.mostrar_total_por_paciente)
        btn_total_pac.grid(row=5, column=2, pady=8)

        ttk.Label(frame, text="ID Factura (buscar):").grid(row=6, column=0, sticky='e')
        self.ent_buscar_fact = ttk.Entry(frame); self.ent_buscar_fact.grid(row=6, column=1)
        btn_buscar = ttk.Button(frame, text="Buscar", command=self.buscar_factura)
        btn_buscar.grid(row=6, column=2)

        ttk.Label(frame, text="ID Factura (actualizar estado):").grid(row=7, column=0, sticky='e')
        self.ent_act_fact = ttk.Entry(frame); self.ent_act_fact.grid(row=7,column=1)
        ttk.Label(frame, text="Nuevo estado:").grid(row=7,column=2, sticky='e')
        self.ent_act_estado = ttk.Entry(frame); self.ent_act_estado.grid(row=7,column=3)
        btn_act = ttk.Button(frame, text="Actualizar estado", command=self.actualizar_estado_factura)
        btn_act.grid(row=7, column=4, padx=5)

        self.txt_fact_result = tk.Text(frame, height=10)
        self.txt_fact_result.grid(row=8, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

        btn_listar = ttk.Button(frame, text="Listar facturas con pacientes", command=self.listar_facturas_pacientes)
        btn_listar.grid(row=9, column=0, pady=5)

        ttk.Label(frame, text="ID Factura (eliminar):").grid(row=10, column=0, sticky='e')
        self.ent_del_fact = ttk.Entry(frame)
        self.ent_del_fact.grid(row=10, column=1, padx=5, pady=5)

        btn_del = ttk.Button(frame, text="Eliminar factura", command=self.eliminar_factura_ui)
        btn_del.grid(row=10, column=2, padx=5, pady=5)
        

    # -- NUEVA FUNCIÓN IMPORTANTE --
    def listar_facturas_pacientes(self):
        datos = dao.listar_facturas_con_pacientes()

        self.txt_fact_result.delete("1.0", tk.END)

        if not datos:
            self.txt_fact_result.insert(tk.END, "No hay facturas registradas.")
            return

        text = ""
        for f in datos:
            text += (
                f"Factura {f['id_factura']} - Paciente: {f['paciente']}\n"
                f"Fecha: {f['fecha']} | Estado: {f['estado_pago']} | "
                f"Monto: {f['monto_total']} | Forma: {f['forma_financiamiento']}\n"
                "---------------------------------------------------------\n"
            )

        self.txt_fact_result.insert(tk.END, text)

    def registrar_factura(self):
        try:
            f = Factura(
                fecha=self.ent_f_fecha.get(),
                estado_pago=self.ent_f_estado.get(),
                forma_financiamiento=self.ent_f_forma.get(),
                monto_total=float(self.ent_f_monto.get()),
                id_paciente=int(self.ent_f_id_pac.get())
            )
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
            return

        ok,msg = dao.registrar_factura(f)
        messagebox.showinfo("Registrar factura", msg if ok else f"Error: {msg}")

    def mostrar_total_general(self):
        total = dao.total_facturado_general()
        messagebox.showinfo("Total general", f"Total facturado: S/. {total:.2f}")

    def mostrar_total_por_paciente(self):
        try:
            idp = int(self.ent_f_id_pac.get())
        except:
            messagebox.showwarning("Total por paciente", "Ingrese un ID válido")
            return
        total = dao.total_facturado_por_paciente(idp)
        messagebox.showinfo("Total por paciente", f"Total facturado al paciente {idp}: S/. {total:.2f}")

    def buscar_factura(self):
        try:
            idf = int(self.ent_buscar_fact.get())
        except:
            messagebox.showwarning("Buscar", "Ingrese ID válido")
            return

        fac = dao.buscar_factura_por_id(idf)
        self.txt_fact_result.delete('1.0', tk.END)

        if not fac:
            self.txt_fact_result.insert(tk.END, "Factura no encontrada.")
            return

        text = (
            f"ID: {fac.id_factura}\nFecha: {fac.fecha}\nEstado: {fac.estado_pago}\n"
            f"Forma: {fac.forma_financiamiento}\nMonto: {fac.monto_total}\nID Paciente: {fac.id_paciente}"
        )
        self.txt_fact_result.insert(tk.END, text)

    def actualizar_estado_factura(self):
        try:
            idf = int(self.ent_act_fact.get())
        except:
            messagebox.showwarning("Actualizar", "ID inválido")
            return

        estado = self.ent_act_estado.get()
        ok,msg = dao.actualizar_estado_pago(idf, estado)
        messagebox.showinfo("Actualizar", msg if ok else f"Error: {msg}")

    def eliminar_factura_ui(self):
        idv = self.ent_del_fact.get()

        if not idv.isdigit():
            messagebox.showwarning("Eliminar factura", "Ingrese un ID válido")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación",
                                    f"¿Seguro que desea eliminar la factura {idv}?")

        if not confirmar:
            return

        ok, msg = dao.eliminar_factura(int(idv))

        if ok:
            messagebox.showinfo("Eliminar factura", msg)
        else:
            messagebox.showerror("Error", msg)

    def build_ficha_medica_tab(self):
        frame = self.tab_fichamedica

    # --- campos ficha ---
        tk.Label(frame, text="ID Paciente:").grid(row=0, column=0)
        self.fm_id_paciente = tk.Entry(frame)
        self.fm_id_paciente.grid(row=0, column=1)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0)
        self.fm_fecha = tk.Entry(frame)
        self.fm_fecha.grid(row=1, column=1)

        tk.Label(frame, text="Marcha:").grid(row=2, column=0)
        self.fm_marcha = tk.Entry(frame, width=40)
        self.fm_marcha.grid(row=2, column=1)

        tk.Label(frame, text="Otros aspectos:").grid(row=3, column=0)
        self.fm_otros = tk.Entry(frame, width=40)
        self.fm_otros.grid(row=3, column=1)

        tk.Label(frame, text="Observaciones médicas:").grid(row=4, column=0)
        self.fm_obs = tk.Entry(frame, width=40)
        self.fm_obs.grid(row=4, column=1)

        tk.Label(frame, text="ID ingreso:").grid(row=5, column=0)
        self.fm_id_ingreso = tk.Entry(frame)
        self.fm_id_ingreso.grid(row=5, column=1)

        tk.Button(
            frame, text="Registrar ficha médica",
            command=self.action_registrar_ficha
        ).grid(row=6, column=1, pady=10)

    # --- Listar fichas ---
        tk.Label(frame, text="ID Paciente:").grid(row=7, column=0)
        self.fm_listar = tk.Entry(frame)
        self.fm_listar.grid(row=7, column=1)

        tk.Button(
            frame, text="Listar fichas",
            command=self.action_listar_fichas
        ).grid(row=7, column=2)

        self.fm_output = tk.Text(frame, width=90, height=15)
        self.fm_output.grid(row=8, column=0, columnspan=3, pady=10)

    # --- Enfermedades ---
        tk.Label(frame, text="ID Ficha:").grid(row=9, column=0)
        self.fm_id_ficha_enf = tk.Entry(frame)
        self.fm_id_ficha_enf.grid(row=9, column=1)

        tk.Label(frame, text="ID Enfermedad:").grid(row=10, column=0)
        self.fm_id_enfermedad = tk.Entry(frame)
        self.fm_id_enfermedad.grid(row=10, column=1)

        tk.Label(frame, text="Tratamiento:").grid(row=11, column=0)
        self.fm_tratamiento = tk.Entry(frame, width=40)
        self.fm_tratamiento.grid(row=11, column=1)

        tk.Button(
            frame, text="Agregar enfermedad",
            command=self.action_insertar_enfermedad
        ).grid(row=12, column=1)

        tk.Button(
            frame, text="Ver enfermedades",
            command=self.action_ver_enfermedades
        ).grid(row=12, column=2)

    def action_registrar_ficha(self):
        from dao import insertar_ficha_medica
        ok = insertar_ficha_medica(
            self.fm_fecha.get(),
            self.fm_marcha.get(),
            self.fm_otros.get(),
            self.fm_obs.get(),
            self.fm_id_paciente.get(),
            self.fm_id_ingreso.get()
        )
        if ok: messagebox.showinfo("OK", "Ficha registrada")


    def action_listar_fichas(self):
        from dao import listar_fichas_por_paciente
        fichas = listar_fichas_por_paciente(self.fm_listar.get())

        self.fm_output.delete("1.0", tk.END)
        for f in fichas:
            self.fm_output.insert(tk.END, f"Ficha {f['id_ficha']} - Fecha: {f['fecha_registro']}\n")
            self.fm_output.insert(tk.END, f"Marcha: {f['marcha']}\n")
            self.fm_output.insert(tk.END, f"Obs: {f['observaciones_medicas']}\n")
            self.fm_output.insert(tk.END, "-"*40 + "\n")


    def action_insertar_enfermedad(self):
        from dao import insertar_enfermedad_en_ficha
        ok = insertar_enfermedad_en_ficha(
            self.fm_id_ficha_enf.get(),
            self.fm_id_enfermedad.get(),
            self.fm_tratamiento.get()
        )
        if ok: messagebox.showinfo("OK", "Enfermedad agregada a ficha")


    def action_ver_enfermedades(self):
        from dao import obtener_enfermedades_de_ficha

        enf = obtener_enfermedades_de_ficha(self.fm_id_ficha_enf.get())
        self.fm_output.delete("1.0", tk.END)

        for e in enf:
            self.fm_output.insert(tk.END, f"{e['nombre']} - {e['tratamiento']}\n")




if __name__ == "__main__":
    app = VitaliaApp()
    app.mainloop()
