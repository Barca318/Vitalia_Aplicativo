@echo off
echo ======================================
echo COMPILANDO EL APLICATIVO VITALIA...
echo ======================================
javac -cp "lib/mysql-connector-j-9.5.0.jar" -d out src/db/Db.java src/ui/Menu.java src/App.java

echo.
echo ======================================
echo EJECUTANDO EL APLICATIVO...
echo ======================================
java -cp "out;lib/mysql-connector-j-9.5.0.jar" App
echo.
pause
