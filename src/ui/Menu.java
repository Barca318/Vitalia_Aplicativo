package ui;
import db.Db;
import java.sql.*;
import java.util.Scanner;

public class Menu {
    private static Scanner sc = new Scanner(System.in);
    public static void mainMenu() {
        while (true) {
            System.out.println("\n=== VITALIA – MENÚ PRINCIPAL ===");
            System.out.println("1. Insertar Paciente");
            System.out.println("2. Actualizar Paciente");
            System.out.println("3. Eliminar Paciente");
            System.out.println("4. Registrar Factura");
            System.out.println("5. Calcular total facturado (función)");
            System.out.println("0. Salir");
            System.out.print("Opción: ");
            int op = Integer.parseInt(sc.nextLine());

            switch (op) {
                case 1 -> insertarPaciente();
                case 2 -> actualizarPaciente();
                case 3 -> eliminarPaciente();
                case 4 -> registrarFactura();
                case 5 -> calcularTotal();
                case 0 -> { System.out.println("Fin del programa."); return; }
                default -> System.out.println("Opción inválida.");
            }
        }
    }

    private static void insertarPaciente() {
        try (Connection cn = Db.conectar()) {
            System.out.print("DNI: "); String dni = sc.nextLine();
            System.out.print("Nombres: "); String nombres = sc.nextLine();
            System.out.print("Apellido paterno: "); String ap = sc.nextLine();
            System.out.print("Apellido materno: "); String am = sc.nextLine();
            System.out.print("Estado civil: "); String ec = sc.nextLine();

            CallableStatement cs = cn.prepareCall("{CALL sp_paciente_insert(?,?,?,?,?)}");
            cs.setString(1, dni);
            cs.setString(2, nombres);
            cs.setString(3, ap);
            cs.setString(4, am);
            cs.setString(5, ec);

            ResultSet rs = cs.executeQuery();
            while (rs.next()) System.out.println(rs.getString(1));

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
    
    private static void actualizarPaciente() {
        try (Connection cn = Db.conectar()) {
            System.out.print("ID del paciente: "); int id = Integer.parseInt(sc.nextLine());
            System.out.print("Nombres: "); String nombres = sc.nextLine();
            System.out.print("Apellido paterno: "); String ap = sc.nextLine();
            System.out.print("Apellido materno: "); String am = sc.nextLine();
            System.out.print("Estado civil: "); String ec = sc.nextLine();
            
            CallableStatement cs = cn.prepareCall("{CALL sp_paciente_update(?,?,?,?,?)}");
            cs.setInt(1, id);
            cs.setString(2, nombres);
            cs.setString(3, ap);
            cs.setString(4, am);
            cs.setString(5, ec);

            ResultSet rs = cs.executeQuery();
            while (rs.next()) System.out.println(rs.getString(1));

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
