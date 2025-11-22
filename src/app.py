# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Paciente, Factura, FichaMedica, Enfermedad, Habitacion, Ingreso
import dao
from tkinter import simpledialog



class VitaliaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vitalia - Registro de Clientes")
        self.geometry("1100x650")
        self.create_widgets()



    def build_dashboard(self):
        self.dashboard = tk.Frame(self, bg="#eef2f3")
        self.dashboard.pack(fill="both", expand=True)

    # Título
        tk.Label(
            self.dashboard, 
            text="VITALIA – Centro Médico",
            font=("Arial", 26, "bold"),
            bg="#eef2f3",
            fg="#2a4d69"
        ).pack(pady=30)

        tk.Label(
            self.dashboard,
            text="Seleccione una opción:",
            font=("Arial", 14),
            bg="#eef2f3",
            fg="#4b4b4b"
        ).pack(pady=10)

    # Contenedor de botones
        container = tk.Frame(self.dashboard, bg="#eef2f3")
        container.pack(pady=20)

        style = ttk.Style()
        style.configure("Big.TButton",
            font=("Arial", 14, "bold"), 
            padding=20
        )

        buttons = [
            ("Pacientes", 0),
            ("Facturas", 1),
            ("Fichas Médicas", 2),
            ("Habitaciones", 3),
            ("Ingresos", 4)
        ]

        for text, tab_index in buttons:
            ttk.Button(
                container,
                text=text,
                style="Big.TButton",
                command=lambda t=tab_index: self.open_tab(t)
            ).pack(pady=10, fill="x", ipadx=20)
        self.dashboard_frame = tk.Frame(self, bg="#FFFFFF")
        self.dashboard_frame.pack(fill="both", expand=True)
    def open_tab(self, index):
        """Oculta el dashboard y abre la pestaña seleccionada."""

    # Ocultar dashboard si existe
        if hasattr(self, "dashboard"):
            self.dashboard.pack_forget()

    # Mostrar notebook
        self.notebook.pack(expand=True, fill="both")

    # Seleccionar pestaña
        self.notebook.select(index)



    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        


        self.tab_pacientes = ttk.Frame(self.notebook)
        self.tab_facturas = ttk.Frame(self.notebook)
        self.tab_fichamedica = ttk.Frame(self.notebook)
        self.tab_habitaciones = ttk.Frame(self.notebook)
        self.tab_ingresos = ttk.Frame(self.notebook)


        self.notebook.add(self.tab_pacientes, text="Pacientes")
        self.notebook.add(self.tab_facturas, text="Facturas")
        self.notebook.add(self.tab_fichamedica, text="Ficha Médica")
        self.notebook.add(self.tab_habitaciones, text="Habitaciones")
        self.notebook.add(self.tab_ingresos, text="Ingresos")
        

        self.build_pacientes_tab()
        self.build_facturas_tab()
        self.build_ficha_medica_tab()
        self.build_habitaciones_tab()
        self.build_ingresos_tab()

        self.build_dashboard()



    # ---------------- Pacientes ----------------
    def build_pacientes_tab(self):
        frame = self.tab_pacientes

        ttk.Label(
            frame,
            text="Gestión de Pacientes",
            font=("Arial", 18, "bold")
        )   .grid(row=0, column=0, columnspan=3, pady=15)
        
        labels = [
            "DNI:", "Nombres:", "Apellido Paterno:", "Apellido Materno:",
            "Fecha Nac (YYYY-MM-DD):",
            "Estado Civil:", "Profesión:", "Calle:", "Número:",
            "Distrito:", "Provincia:", "Número de Hijos:", "Observaciones:"
        ]
        
        self.entries = []
        row = 1
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

        ttk.Button(frame, text="Insertar", command=self.insertar_paciente).grid(row=row, column=0, pady=10)
        ttk.Button(frame, text="Actualizar (por ID)", command=self.actualizar_paciente).grid(row=row, column=1, pady=10)
        ttk.Button(frame, text="Eliminar (por ID)", command=self.eliminar_paciente).grid(row=row, column=2, pady=10)

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

        self.tree_pacientes.grid(row=row, column=0, columnspan=4, sticky='nsew', pady=10)
        frame.grid_rowconfigure(row, weight=1)

        ttk.Button(frame, text="Refrescar lista", command=self.refrescar_pacientes).grid(row=row+1, column=0, pady=5)

        ttk.Button(frame, text="Volver al menú", command=self.go_dashboard).grid(row=row+2, column=0, pady=10)


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

    def go_dashboard(self):
    
        self.notebook.pack_forget()

        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)


    
    # ---------------- Facturas ----------------
    def build_facturas_tab(self):
        frame = self.tab_facturas

        ttk.Label(
            frame,
            text="Gestión de Facturas",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=5, pady=15)

        
        ttk.Label(frame, text="ID Paciente:").grid(row=1, column=0, sticky='e')
        self.ent_f_id_pac = ttk.Entry(frame); self.ent_f_id_pac.grid(row=1,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.ent_f_fecha = ttk.Entry(frame); self.ent_f_fecha.grid(row=2,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Estado pago:").grid(row=3, column=0, sticky='e')
        self.ent_f_estado = ttk.Entry(frame); self.ent_f_estado.grid(row=3,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Forma financiamiento:").grid(row=4, column=0, sticky='e')
        self.ent_f_forma = ttk.Entry(frame); self.ent_f_forma.grid(row=4,column=1,padx=5,pady=5)

        ttk.Label(frame, text="Monto total:").grid(row=5, column=0, sticky='e')
        self.ent_f_monto = ttk.Entry(frame); self.ent_f_monto.grid(row=5,column=1,padx=5,pady=5)

        btn_reg = ttk.Button(frame, text="Registrar factura", command=self.registrar_factura)
        btn_reg.grid(row=6, column=0, pady=8)
        btn_total = ttk.Button(frame, text="Total general", command=self.mostrar_total_general)
        btn_total.grid(row=6, column=1, pady=8)
        btn_total_pac = ttk.Button(frame, text="Total por paciente", command=self.mostrar_total_por_paciente)
        btn_total_pac.grid(row=6, column=2, pady=8)


        btn_promos = ttk.Button(frame, text="Ver promociones", command=self.mostrar_promociones)
        btn_promos.grid(row=6, column=3, pady=8)



        ttk.Label(frame, text="ID Factura (buscar):").grid(row=7, column=0, sticky='e')
        self.ent_buscar_fact = ttk.Entry(frame); self.ent_buscar_fact.grid(row=7, column=1)
        btn_buscar = ttk.Button(frame, text="Buscar", command=self.buscar_factura)
        btn_buscar.grid(row=7, column=2)

        ttk.Label(frame, text="ID Factura (actualizar estado):").grid(row=8, column=0, sticky='e')
        self.ent_act_fact = ttk.Entry(frame); self.ent_act_fact.grid(row=8,column=1)
        ttk.Label(frame, text="Nuevo estado:").grid(row=8,column=2, sticky='e')
        self.ent_act_estado = ttk.Entry(frame); self.ent_act_estado.grid(row=8,column=3)
        btn_act = ttk.Button(frame, text="Actualizar estado", command=self.actualizar_estado_factura)
        btn_act.grid(row=8, column=4, padx=5)

        self.txt_fact_result = tk.Text(frame, height=10)
        self.txt_fact_result.grid(row=9, column=0, columnspan=5, padx=5, pady=5, sticky='nsew')

        btn_listar = ttk.Button(frame, text="Listar facturas con pacientes", command=self.listar_facturas_pacientes)
        btn_listar.grid(row=10, column=0, pady=5)

        ttk.Label(frame, text="ID Factura (eliminar):").grid(row=11, column=0, sticky='e')
        self.ent_del_fact = ttk.Entry(frame)
        self.ent_del_fact.grid(row=11, column=1, padx=5, pady=5)

        btn_del = ttk.Button(frame, text="Eliminar factura", command=self.eliminar_factura_ui)
        btn_del.grid(row=11, column=2, padx=5, pady=5)
        
        btn_plan = ttk.Button(frame, text="Asignar Plan al Paciente", command=self.asignar_plan_ui)
        btn_plan.grid(row=12, column=0, pady=8)

        
        ttk.Button(frame, text="Volver al menú", command=self.go_dashboard).grid(row=13, column=0, pady=10)




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

    def mostrar_promociones(self):
        promos = dao.listar_promociones()

        if not promos:
            messagebox.showinfo("Promociones", "No hay promociones registradas.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Promociones Disponibles")
        ventana.geometry("500x300")

        tree = ttk.Treeview(
            ventana,
            columns=("id", "nombre", "descripcion", "descuento"),
            show="headings",
            height=10
        )

        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("descripcion", text="Descripción")
        tree.heading("descuento", text="Descuento (%)")

        tree.column("id", width=60)
        tree.column("nombre", width=150)
        tree.column("descripcion", width=200)
        tree.column("descuento", width=90)

        for promo in promos:
            tree.insert("", tk.END, values=(
                promo["id_promo"],
                promo["nombre_promo"],
                promo["descripcion"],
                promo["descuento"]
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def aplicar_promocion_ui(self):
        id_promo = simpledialog.askinteger(
            "Aplicar promoción",
            "Ingrese el ID de la promoción:"
        )

        if not id_promo:
            return

        promos = dao.listar_promociones()
        promo = next((p for p in promos if p["id_promo"] == id_promo), None)

        if not promo:
            messagebox.showerror("Error", "No existe una promoción con ese ID.")
            return

        try:
            monto = float(self.ent_f_monto.get())
        except:
            messagebox.showerror("Error", "Debe ingresar primero un monto válido.")
            return

        descuento = promo["descuento"]
        nuevo_monto = monto - (monto * descuento / 100)

        self.ent_f_monto.delete(0, tk.END)
        self.ent_f_monto.insert(0, f"{nuevo_monto:.2f}")

        messagebox.showinfo(
            "Promoción aplicada",
            f"Se aplicó '{promo['nombre_promo']}' (-{descuento}%).\n"
            f"Nuevo monto: {nuevo_monto:.2f}"
        )

    def asignar_plan_ui(self):
        
        id_pac = simpledialog.askinteger("ID Paciente", "Ingrese ID del paciente:")
        if not id_pac:
            return


        planes = dao.listar_planes()
        if not planes:
            messagebox.showerror("Error", "No hay planes registrados.")
            return

        opciones = "\n".join([f"{p['id_plan']} - {p['nombre_plan']} (S/.{p['tarifa']})" for p in planes])
        messagebox.showinfo("Planes disponibles", opciones)


        id_plan = simpledialog.askinteger("Elegir Plan", "Seleccione ID del plan:")
        if not id_plan:
            return

        ok, msg = dao.registrar_factura_plan(id_pac, id_plan)

        messagebox.showinfo("Resultado", msg)

        if ok:
            self.txt_fact_result.insert(tk.END, f"\nFactura generada con plan {id_plan} para paciente {id_pac}\n")



    def go_dashboard(self):
    
        self.notebook.pack_forget()

        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)

    def build_ficha_medica_tab(self):
        frame = self.tab_fichamedica

        ttk.Label(
            frame,
            text="Gestión de Fichas Médicas",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=15)
        
        
        tk.Label(frame, text="ID Paciente:").grid(row=1, column=0)
        self.fm_id_paciente = tk.Entry(frame)
        self.fm_id_paciente.grid(row=1, column=1)

        tk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0)
        self.fm_fecha = tk.Entry(frame)
        self.fm_fecha.grid(row=2, column=1)

        tk.Label(frame, text="Marcha:").grid(row=3, column=0)
        self.fm_marcha = tk.Entry(frame, width=40)
        self.fm_marcha.grid(row=3, column=1)

        tk.Label(frame, text="Otros aspectos:").grid(row=4, column=0)
        self.fm_otros = tk.Entry(frame, width=40)
        self.fm_otros.grid(row=4, column=1)

        tk.Label(frame, text="Observaciones médicas:").grid(row=5, column=0)
        self.fm_obs = tk.Entry(frame, width=40)
        self.fm_obs.grid(row=5, column=1)

        tk.Label(frame, text="ID ingreso:").grid(row=6, column=0)
        self.fm_id_ingreso = tk.Entry(frame)
        self.fm_id_ingreso.grid(row=6, column=1)

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
        
        ttk.Button(frame, text="Volver al menú", command=self.go_dashboard).grid(row=14, column=0, pady=10)

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

    def go_dashboard(self):

        self.notebook.pack_forget()


        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)

    def go_dashboard(self):
    
        self.notebook.pack_forget()

        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)

    def build_habitaciones_tab(self):
        frame = self.tab_habitaciones


        tk.Label(frame, text="Gestión de Habitaciones", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)


        tk.Label(frame, text="Número:").grid(row=1, column=0, sticky="e", padx=5)
        self.hab_buscar_num = tk.Entry(frame, width=15)
        self.hab_buscar_num.grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Tipo:").grid(row=1, column=2, sticky="e", padx=5)
        self.hab_buscar_tipo = ttk.Combobox(frame, values=["Individual", "Doble", "Suite"], width=12)
        self.hab_buscar_tipo.grid(row=1, column=3, padx=5)

        tk.Label(frame, text="Estado:").grid(row=1, column=4, sticky="e", padx=5)
        self.hab_buscar_estado = ttk.Combobox(frame, values=["Disponible", "Ocupada", "Mantenimiento"], width=15)
        self.hab_buscar_estado.grid(row=1, column=5, padx=5)

        ttk.Button(frame, text="Buscar", command=self.ui_buscar_habitaciones)\
            .grid(row=1, column=6, padx=10)

        cols = ("ID", "Número", "Tipo", "Estado")
        self.tree_habitaciones = ttk.Treeview(frame, columns=cols, show="headings", height=12)

        for col in cols:
            self.tree_habitaciones.heading(col, text=col)
            self.tree_habitaciones.column(col, width=120)

        self.tree_habitaciones.grid(row=2, column=0, columnspan=7, pady=10)


        ttk.Button(frame, text="Nueva Habitación", command=self.ui_nueva_habitacion)\
            .grid(row=3, column=0, pady=10)

        ttk.Button(frame, text="Actualizar Habitación", command=self.ui_actualizar_habitacion)\
            .grid(row=3, column=1, pady=10)

        ttk.Button(frame, text="Eliminar Habitación", command=self.ui_eliminar_habitacion)\
            .grid(row=3, column=2, pady=10)

        ttk.Button(frame, text="Refrescar Lista", command=self.refresh_habitaciones)\
            .grid(row=3, column=3, pady=10)

        ttk.Button(frame, text="Volver al menú", command=self.go_dashboard).grid(row=5, column=0, pady=10)

        self.refresh_habitaciones()

    def ui_buscar_habitaciones(self):
        from dao import buscar_habitacion

        num = self.hab_buscar_num.get().strip()
        tipo = self.hab_buscar_tipo.get().strip()
        estado = self.hab_buscar_estado.get().strip()

        rows = buscar_habitacion(
            num_habitacion=num if num else None,
            estado=estado if estado else None,
            tipo_habitacion=tipo if tipo else None
        )

        for item in self.tree_habitaciones.get_children():
            self.tree_habitaciones.delete(item)

        for r in rows:
            self.tree_habitaciones.insert(
                "", "end",
                values=(r["id_habitacion"], r["num_habitacion"], r["tipo_habitacion"], r["estado"])
            )

    def ui_nueva_habitacion(self):
        win = tk.Toplevel(self)
        win.title("Registrar Habitación")
        win.geometry("280x230")

        tk.Label(win, text="Número:").pack()
        e_num = tk.Entry(win)
        e_num.pack()

        tk.Label(win, text="Tipo:").pack()
        e_tipo = ttk.Combobox(win, values=["Individual", "Doble", "Suite"])
        e_tipo.pack()

        tk.Label(win, text="Estado:").pack()
        e_estado = ttk.Combobox(win, values=["Disponible", "Ocupada", "Mantenimiento"])
        e_estado.set("Disponible")
        e_estado.pack()

        def guardar():
            from dao import insertar_habitacion
            from models import Habitacion

            h = Habitacion(
                id_habitacion=None,
                num_habitacion=e_num.get(),
                tipo_habitacion=e_tipo.get(),
                estado=e_estado.get()
            )

            ok = insertar_habitacion(h)
            messagebox.showinfo("Resultado", "Guardado correctamente" if ok else "Error")
            win.destroy()
            self.refresh_habitaciones()

        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)


    def ui_actualizar_habitacion(self):
        sel = self.tree_habitaciones.selection()
        if not sel:
            messagebox.showwarning("Actualizar", "Seleccione una habitación")
            return

        valores = self.tree_habitaciones.item(sel[0])["values"]
        id_hab, num0, tipo0, estado0 = valores

        win = tk.Toplevel(self)
        win.title("Actualizar Habitación")
        win.geometry("300x250")

        tk.Label(win, text="Número:").pack()
        e_num = tk.Entry(win)
        e_num.insert(0, num0)
        e_num.pack()

        tk.Label(win, text="Tipo:").pack()
        e_tipo = ttk.Combobox(win, values=["Individual", "Doble", "Suite"])
        e_tipo.set(tipo0)
        e_tipo.pack()

        tk.Label(win, text="Estado:").pack()
        e_estado = ttk.Combobox(win, values=["Disponible", "Ocupada", "Mantenimiento"])
        e_estado.set(estado0)
        e_estado.pack()

        def guardar():
            from dao import actualizar_habitacion
            from models import Habitacion

            h = Habitacion(
                id_habitacion=id_hab,
                num_habitacion=e_num.get(),
                tipo_habitacion=e_tipo.get(),
                estado=e_estado.get()
            )

            ok = actualizar_habitacion(h)
            messagebox.showinfo("Actualizar", "Actualizado" if ok else "Error")
            win.destroy()
            self.refresh_habitaciones()

        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)


    def ui_eliminar_habitacion(self):
        sel = self.tree_habitaciones.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Seleccione una habitación")
            return

        id_hab = self.tree_habitaciones.item(sel[0])["values"][0]

        confirmar = messagebox.askyesno("Eliminar", f"¿Eliminar habitación {id_hab}?")
        if not confirmar:
            return

        from dao import eliminar_habitacion
        ok, msg = eliminar_habitacion(id_hab)

        if ok:
            messagebox.showinfo("Eliminar", msg)
        else:
            messagebox.showerror("Error", msg)

        self.refresh_habitaciones()
        
    def refresh_habitaciones(self):
        from dao import listar_habitaciones

        rows = listar_habitaciones()

        for item in self.tree_habitaciones.get_children():
            self.tree_habitaciones.delete(item)

        for h in rows:
            self.tree_habitaciones.insert(
                "", "end",
                values=(h.id_habitacion, h.num_habitacion, h.tipo_habitacion, h.estado)
            )

    def go_dashboard(self):
    
        self.notebook.pack_forget()

        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)

    def build_ingresos_tab(self):
        frame = self.tab_ingresos

  
        ttk.Label(frame, text="Gestión de Ingresos", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

    
        ttk.Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0)
        self.ing_fecha = ttk.Entry(frame)
        self.ing_fecha.grid(row=1, column=1)

        ttk.Label(frame, text="ID Paciente:").grid(row=2, column=0)
        self.ing_paciente = ttk.Entry(frame)
        self.ing_paciente.grid(row=2, column=1)

        ttk.Label(frame, text="ID Habitación:").grid(row=3, column=0)
        self.ing_habitacion = ttk.Entry(frame)
        self.ing_habitacion.grid(row=3, column=1)

        ttk.Label(frame, text="ID Plan:").grid(row=4, column=0)
        self.ing_plan = ttk.Entry(frame)
        self.ing_plan.grid(row=4, column=1)


        ttk.Button(frame, text="Registrar Ingreso",
               command=self.ui_registrar_ingreso).grid(row=5, column=0, columnspan=2, pady=10)

        cols = ("ID", "Fecha", "Paciente", "Habitación", "Plan")
        self.ingresos_tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)

        for c in cols:
            self.ingresos_tree.heading(c, text=c)
            self.ingresos_tree.column(c, width=150)

        self.ingresos_tree.grid(row=6, column=0, columnspan=4, pady=10)

        ttk.Label(frame, text="ID Ingreso:").grid(row=9, column=0)
        self.ing_edit_id = ttk.Entry(frame, width=10)
        self.ing_edit_id.grid(row=9, column=1)

        ttk.Button(frame, text="Cargar Datos", command=self.ui_cargar_ingreso).grid(row=9, column=2, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.ui_eliminar_ingreso).grid(row=9, column=3, padx=5)

# Campos para edición
        ttk.Label(frame, text="Nueva Fecha:").grid(row=10, column=0)
        self.ing_edit_fecha = ttk.Entry(frame)
        self.ing_edit_fecha.grid(row=10, column=1)

        ttk.Label(frame, text="Nuevo Paciente:").grid(row=11, column=0)
        self.ing_edit_paciente = ttk.Entry(frame)
        self.ing_edit_paciente.grid(row=11, column=1)

        ttk.Label(frame, text="Nueva Habitación:").grid(row=12, column=0)
        self.ing_edit_habitacion = ttk.Entry(frame)
        self.ing_edit_habitacion.grid(row=12, column=1)

        ttk.Label(frame, text="Nuevo Plan:").grid(row=13, column=0)
        self.ing_edit_plan = ttk.Entry(frame)
        self.ing_edit_plan.grid(row=13, column=1)

        ttk.Button(frame, text="Guardar Cambios",
           command=self.ui_guardar_cambios_ingreso).grid(row=14, column=1, pady=10)
        
        ttk.Button(frame, text="Actualizar Lista", command=self.refresh_ingresos).grid(row=7, column=0, pady=10)

        ttk.Label(frame, text="Historial por habitación:").grid(row=8, column=0)
        self.hist_hab = ttk.Entry(frame)
        self.hist_hab.grid(row=8, column=1)
        ttk.Button(frame, text="Ver", command=self.ui_historial_habitacion).grid(row=8, column=2)
        
        ttk.Button(frame, text="Volver al menú", command=self.go_dashboard).grid(row=18, column=0, pady=10)

        self.refresh_ingresos()

    def ui_registrar_ingreso(self):
        from dao import registrar_ingreso
        from models import Ingreso

        try:
            ingreso = Ingreso(
                id_ingreso=None,
                fecha_ingreso=self.ing_fecha.get(),
                id_paciente=int(self.ing_paciente.get()),
                id_habitacion=int(self.ing_habitacion.get()),
                id_plan=int(self.ing_plan.get())
            )
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = registrar_ingreso(ingreso)
        messagebox.showinfo("Resultado", msg)
        self.refresh_ingresos()
    
    def ui_cargar_ingreso(self):
        from dao import listar_ingresos

        ing_id = self.ing_edit_id.get()
        if not ing_id.isdigit():
            messagebox.showwarning("Error", "ID inválido")
            return

        data = listar_ingresos()

        row = next((x for x in data if str(x["id_ingreso"]) == ing_id), None)

        if not row:
            messagebox.showerror("Error", "Ingreso no encontrado")
            return

    # Guardamos la habitación anterior para actualizar
        self.ing_hab_anterior = row["id_habitacion"]

    # Cargamos en los campos
        self.ing_edit_fecha.delete(0, "end")
        self.ing_edit_fecha.insert(0, row["fecha_ingreso"])

        self.ing_edit_paciente.delete(0, "end")
        self.ing_edit_paciente.insert(0, row["id_paciente"])

        self.ing_edit_habitacion.delete(0, "end")
        self.ing_edit_habitacion.insert(0, row["id_habitacion"])

        self.ing_edit_plan.delete(0, "end")
        self.ing_edit_plan.insert(0, row["id_plan"])

        messagebox.showinfo("OK", "Datos cargados")

    
    def ui_guardar_cambios_ingreso(self):
        from dao import editar_ingreso
        from models import Ingreso

        ing_id = self.ing_edit_id.get()
        if not ing_id.isdigit():
            messagebox.showwarning("Error", "ID inválido")
            return

        try:
            ingreso = Ingreso(
                id_ingreso=int(ing_id),
                fecha_ingreso=self.ing_edit_fecha.get(),
                id_paciente=int(self.ing_edit_paciente.get()),
                id_habitacion=int(self.ing_edit_habitacion.get()),
                id_plan=int(self.ing_edit_plan.get())
            )
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = editar_ingreso(ingreso, self.ing_hab_anterior)
        if ok:
            messagebox.showinfo("OK", msg)
            self.refresh_ingresos()
        else:
            messagebox.showerror("Error", msg)
    
    
    def ui_eliminar_ingreso(self):
        from dao import eliminar_ingreso
        from dao import listar_ingresos

        ing_id = self.ing_edit_id.get()
        if not ing_id.isdigit():
            messagebox.showwarning("Error", "ID inválido")
            return

        data = listar_ingresos()
        row = next((x for x in data if str(x["id_ingreso"]) == ing_id), None)

        if not row:
            messagebox.showerror("Error", "Ingreso no existe")
            return

        hab = row["id_habitacion"]

        ok, msg = eliminar_ingreso(int(ing_id), hab)

        if ok:
            messagebox.showinfo("OK", "Ingreso eliminado")
            self.refresh_ingresos()
        else:
            messagebox.showerror("Error", msg)

        
    
    def refresh_ingresos(self):
        from dao import listar_ingresos
        data = listar_ingresos()

        for i in self.ingresos_tree.get_children():
            self.ingresos_tree.delete(i)

        for r in data:
            self.ingresos_tree.insert("", "end", values=(
                r["id_ingreso"],
                r["fecha_ingreso"],
                r["paciente"],
                r["habitacion"],
                r["id_plan"]
            ))

    def ui_historial_habitacion(self):
        from dao import historial_habitacion

        hab = self.hist_hab.get()
        if not hab.isdigit():
            messagebox.showwarning("Error", "ID inválido")
            return

        data = historial_habitacion(int(hab))
        txt = "\n".join([f"{i['id_ingreso']} - {i['fecha_ingreso']} - Paciente {i['id_paciente']}" for i in data])

        messagebox.showinfo("Historial", txt if txt else "No hay registros")

    def go_dashboard(self):
    
        self.notebook.pack_forget()

        if hasattr(self, "dashboard"):
            self.dashboard.pack(fill="both", expand=True)
            
            

if __name__ == "__main__":
    app = VitaliaApp()
    app.mainloop()
