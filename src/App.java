import db.Db;
import java.sql.*;

public class App {

   public static void main(String[] args){
   Connection cn = DB.Db.conectar();
   if (cn !=null){
    try{
        Statement st = cn.createStatement();
        ResultSet rs = st.executeQuery("SELECT dni,nombres FROM paciente LIMIT 5;");
        System.out.println("Listado de pacientes");
        while (rs.next()){
            System.out.println(rs.getString("dni")+ "-" + rs.getString("nombres"));
        }
        cn.close();

    } catch(SQLException e){
        System.out.println("Error al consultar:" + e.getMessage());
        }
   }
   } 
}