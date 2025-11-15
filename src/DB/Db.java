package DB;
import java.sql.*;

public class Db {
    private static final String URL  = "jdbc:mysql://localhost:3306/vitalia_db?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASS = "root";

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            System.err.println("No se encontró el driver JDBC de MySQL en el classpath: " + e.getMessage());
        }
    }

    public static Connection conectar() {
        try {
            Connection cn = DriverManager.getConnection(URL, USER, PASS);
            System.out.println("Conexión establecida correctamente con la base de datos Vitalia.");
            return cn;
        } catch (SQLException e) {
            System.out.println("Error de conexión: " + e.getMessage());
            return null;
        }
    }
}
