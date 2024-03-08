from flask import Flask, render_template, request, redirect, url_for, flash,send_file
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/download-file', methods=['POST'])
def download_file():
    try:
        # Path to the file downloaded by Selenium within the Docker volume
        file_path = '/shared/file_example_XLS_10.xls'

        # Serve the file for download
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        raise Exception(e)
# Endpoint to trigger automation tasks
@app.route('/automate_firefox')
def automate_firefox():
    try:
        # Initialize Selenium WebDriver with Firefox options
        options = FirefoxOptions()
        options.headless = False # Set to False if you want to see the browser UI
        driver = webdriver.Remote(command_executor='http://172.17.0.2:4444', options=options)
        
        # Example automation task: Navigate to a URL and extract its title
        driver.get('https://www.cmu.edu/ira/CDS/pdf/cds_2022_23/general-information.pdf')
        driver.maximize_window()
        # time.sleep(2)
        # # Your automation code here
        # # For example:
        # driver.find_element(By.ID,'L2AGLb').click()
        # time.sleep(2)

        # driver.find_element(By.NAME,'q').send_keys('Este es un ejemplo de automatizacion sin aplicación.', Keys.RETURN)
        time.sleep(200)
        driver.quit()
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
