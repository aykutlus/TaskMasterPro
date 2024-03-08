from flask import Flask, render_template, request, redirect, url_for, flash,send_file
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
from methods.extraido import run_extraido
from methods.termianado import run_termianado

app = Flask(__name__)
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

@app.route('/run-process')
def run_process(username, password, export, frequency, process):
    try:
        if(process == "extraido"):
            # Initialize Selenium WebDriver with Firefox options
            # options = FirefoxOptions()
            # options.headless = False # Set to False if you want to see the browser UI
            # driver = webdriver.Remote(command_executor='http://172.17.0.2:4444', options=options)
            
            run_extraido(username,password, export, frequency)
            
        if(process == "termianado"):
            run_termianado(username,password, export, frequency)
            
    except Exception as e:
            raise Exception(e)
    
    
    
    
# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace with your actual verification process
        if username == 'admin' and password == 'admin':
            return redirect(url_for('dashboard'))  # Redirect to another page
        else:
            flash('Login was unsuccessful. Please check username and password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/projects')
def dashboard():
    return render_template('projects.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
