package db;

import java.sql.Connection;
import java.sql.DriverManager;

public class Db {
    private static final String URL  = "jdbc:mysql://localhost:3306/vitalia_db?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASS = "1";

    public static Connection conectar() {
        try {
            Connection cn = DriverManager.getConnection(URL, USER, PASS);
            return cn;
        } catch (Exception e) {
            System.out.println("Error al conectar a la BD: " + e.getMessage());
            return null;
        }
    }
}
