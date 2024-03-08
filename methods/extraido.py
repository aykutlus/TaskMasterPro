from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
from datetime import datetime, timedelta
import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def run_extraido(username, password, export, frequency):
    print("opening")
    options = FirefoxOptions()
    options.headless = False # Set to False if you want to see the browser UI
    driver = webdriver.Remote(command_executor='http://172.17.0.2:4444', options=options)
    print("opening")
    driver.get("https://chat.openai.com/")
    print("opened")
    time.sleep(1000)
    # # get google.co.in
    driver.get("http://192.168.100.183:18001/sislog/autenticacion/login.do")

    # # Maximize the window and let code stall 
    # # for 10s to properly maximise the window.
    driver.maximize_window()
    time.sleep(2)

    ## 1. AUTHENTICATION
    username = driver.find_element(By.ID, "usuario")
    password = driver.find_element(By.ID, "clave")

    username.send_keys(username)
    password.send_keys(password)

    accept_button = driver.find_element(By.XPATH, value="//input[@value='Aceptar']")
    accept_button.click()
    time.sleep(2)

    ## 2. SELECT ALMACEN
    driver.find_element(By.CLASS_NAME, "botonProducto.botonAlmacen").click()
    time.sleep(2)

    # 3. SELECT ACEPTAR
    frame_name_or_id = "1"  # Replace with the actual frame name or ID
    driver.switch_to.frame(frame_name_or_id)
    time.sleep(1)

    driver.find_element(By.CLASS_NAME, "button.aceptar").click()
    time.sleep(3)

    driver.switch_to.default_content()
    time.sleep(2)

    # 4. SELECT SALIDAS
    control = driver.find_element(By.ID, "a_2110-12")
    control.click()
    time.sleep(2)

    # 5. SELECT CONSULTA DE PEDIDOS
    informes = driver.find_element(By.ID, "a_1056-12")
    informes.click()
    time.sleep(2)

    # 6. SELECT DROPDOWN
    dropdown = driver.find_element(By.ID, "c_sitped")
    select = Select(dropdown)
    select.select_by_value("EX")
    time.sleep(2)


    ## 9. SELECT DESDE
    desde = driver.find_element(By.ID, "d_fecha_desde")
    desde.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
    desde.send_keys(Keys.BACKSPACE)  # Delete the selected text
    desde_hour = datetime.datetime.now()
    yesterday = desde_hour - timedelta(days=1)
    desde_day_string = yesterday.strftime('%d/%m/%Y')
    print(desde_day_string)
    desde.send_keys(desde_day_string)


    ## 9. SELECT HASTA
    hasta = driver.find_element(By.ID, "d_fecha_hasta")
    hasta.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
    hasta.send_keys(Keys.BACKSPACE)  # Delete the selected text
    hasta_time = datetime.datetime.now()
    hasta_day_string = hasta_time.strftime('%d/%m/%Y')
    print(hasta_day_string)
    hasta.send_keys(hasta_day_string)

    ## 9. SELECT BUSCAR
    time.sleep(2)
    accept_button = driver.find_element(By.XPATH, value="//input[@value='Buscar']")
    accept_button.click()

    if(export == 'export'):
        
        ## 10. ORDENADOR POR AGENCIA
        agencia = None

        while agencia is None:
            try:
                agencia = driver.find_element(By.XPATH,"//a[contains(text(), 'Agencia')]")
                time.sleep(2)
            except Exception:
                pass  # Continue waiting until the element is found

        agencia.click()
        time.sleep(2)
            
        ## 10. DOWNLOAD EXCEL
        buton_excel = None

        while buton_excel is None:
            try:
                buton_excel = driver.find_element(By.CSS_SELECTOR, value='span.export.excel')
                time.sleep(2)
            except Exception:
                pass  # Continue waiting until the element is found

        buton_excel.click()

        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(1)
        print(Fore.YELLOW,f"Descargando...")
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(10)


    while True:
        try:
            ## 10. SELECT ARROW
            arrow = driver.find_element(By.ID, "img_display_cabFilter")
            arrow.click()
            time.sleep(3)

            ## 9. SELECT BUSCAR
            accept_button = driver.find_element(By.XPATH, value="//input[@value='Buscar']")
            accept_button.click()
            print(Fore.YELLOW,"Ultima actualizacion: " + datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))
            time.sleep(frequency*60)

        except Exception as e:
            print(Fore.LIGHTBLACK_EX, e)
            print(Fore.RED,f"Boton 'flecha' o boton 'buscar' no estan visibles.")
            time.sleep(1)
            print(Fore.RED,f"Actualizacion reiniciará en 10 segundos. - {datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')}") 
            time.sleep(1)
            print(Fore.RED,f"Importante!!!") 
            time.sleep(1)
            print(Fore.RED,f"Asegurase de estar en la pagina correcta y MAS IMPORTANTE el boton 'FILTRO DE BUSQUEDA' colapsado!")
            time.sleep(10)
            continue