from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

# Configura la conexión a SQL Server
def get_db_connection():
    #Funcion para conectar a BD
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=mssql-180519-0.cloudclusters.net,10034;'  
        'DATABASE=Juan;'
        'UID=Admin;'
        'PWD=Db12345678;'
        'Encrypt=no;'  # Deshabilitar SSL solo para pruebas
    )
    return conn

@app.route('/')
def index():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NombreDeLaTabla")
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"An error occurred: {e}"

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
