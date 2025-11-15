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
    
    
}
