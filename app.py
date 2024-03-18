from flask import Flask, render_template, request, redirect, url_for, flash,send_file,jsonify,make_response 
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
from methods.sislog.extraido.extraido import run_extraido
from methods.sislog.termianado import run_termianado
from methods.sislog.control_de_preparacion import run_control_de_preparacion
from methods.sislog.extraido.extraido_descarga_excel import run_extraido_descarga_excel
from methods.sislog.rendimientos.rendimientos import run_rendimientos
from methods.sislog.rendimientos.descarga_excel import run_rendimientos_descarga_excel

from methods.sage.descarga_devolucion_tienda import run_devolucion_tienda

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/download-file', methods=['POST'])
def download_file():
    try:
        # Path to the directory containing the files
        directory_path = '/shared/'

        # Get a list of files in the directory
        files = os.listdir(directory_path)

        # Find the last modified file
        last_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))

        # Serve the last modified file for download
        file_path = os.path.join(directory_path, last_file)
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return str(e)

@app.route('/run-process', methods=['POST','OPTIONS'])
def run_process():
    try:    
        app.logger.debug('Method: %s', request.method)
        app.logger.debug('Headers: %s', request.headers)
        if request.is_json:
            data = request.get_json()
            print(data)
            # Extract data
            process = data.get('processType')
            operation = data.get('operation')
            username = data.get('username')
            password = data.get('password')
            frequency = data.get('frequency')
            
            if(process == "extraido"):
                if(operation == "export"):
                    run_extraido_descarga_excel(username,password)
                if(operation == "run"):
                    run_extraido(username,password,frequency)
                    
            if(process == "rendimientos"):
                if(operation == "export"):
                    run_rendimientos_descarga_excel(username,password)
                if(operation == "run"):
                    run_rendimientos(username,password,frequency)                    
                    
            if(process == "termianado"):
                run_termianado(username,password,frequency) 
                
            if(process == "devolucionTienda"):
                run_devolucion_tienda(username,password)      
                      
            if(process == "controlPreparacion"):
                run_control_de_preparacion(username,password,frequency)                      
                
                
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Request must be JSON"}), 400     

            
    except Exception as e:
            raise Exception(e)
    
    
    
    
# Route to render the index.html template
@app.route('/')
def index():
    lang = request.args.get('lang', 'en')  # Default language is English
    return render_template('index.html', lang=lang)

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = request.args.get('lang', 'en')  # Default language is English
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace with your actual verification process
        if username == 'admin' and password == 'admin':
            return redirect(url_for('dashboard',lang=lang))  # Redirect to another page
        else:
            if lang == 'es':
                flash('El inicio de sesión no fue exitoso. Por favor, verifique el nombre de usuario y la contraseña', 'error')
            else:
                flash('Login was unsuccessful. Please check username and password', 'error')
            return redirect(url_for('login',lang=lang))
    return render_template('login.html',lang=lang)

@app.route('/projects')
def dashboard():
    lang = request.args.get('lang', 'en')  # Default language is English
    return render_template('projects.html',lang=lang)

@app.route('/agents')
def agents():
    return redirect("http://localhost:4446/ui")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
