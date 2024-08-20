from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)


# Configura la conexión a SQL Server
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=mssql-180519-0.cloudclusters.net,10034;'
        'DATABASE=TareaUno;'
        'UID=Admin;'
        'PWD=Db12345678;'
        'Encrypt=no;'  # Deshabilitar SSL solo para pruebas
    )
    return conn

def prueba():
    return

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_GetEmpleadosOrdenados")
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"Ocurrió un error: {e}"

    return render_template('index.html', data=data)


# Ruta para insertar un nuevo empleado
@app.route('/insert', methods=['POST'])
def insert():
    nombre = request.form['nombre']
    salario = request.form['salario']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.sp_InsertEmpleado ?, ?", (nombre, salario))
        conn.commit()
        message = "Empleado insertado correctamente."
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '50001':
            message = "Error: El empleado ya existe en la base de datos."
        elif sqlstate == '50002':
            message = "Error: El salario no puede ser NULL y debe ser un valor positivo."
        elif sqlstate == '50003':
            message = "Error: El nombre no puede ser NULL, vacío, y debe contener solo letras y guiones."
        else:
            message = f"Error inesperado: {ex}"
    finally:

        cursor.close()
        conn.close()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_GetEmpleadosOrdenados")
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"Ocurrió un error: {e}"

    return render_template('index.html', data=data, mensaje=message)

if __name__ == '__main__':
    app.run(debug=True)
