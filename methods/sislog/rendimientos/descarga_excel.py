
# import webdriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from colorama import init, Fore
from datetime import datetime, timedelta
import datetime
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def get_last_sunday(date):
    # Find the current day of the week (0 = Monday, 6 = Sunday)
    current_day = date.weekday()
    # Calculate the days needed to go back to the previous Sunday
    days_to_last_sunday = current_day + 1
    # Calculate the last Sunday date
    last_sunday = date - timedelta(days=days_to_last_sunday)
    return last_sunday

def get_sunday_two_weeks_ago(date):
    # Find the current day of the week (0 = Monday, 6 = Sunday)
    current_day = date.weekday()
    # Calculate the days needed to go back to the Sunday two weeks ago
    days_to_two_weeks_ago_sunday = current_day + 8
    # Calculate the Sunday two weeks ago date
    two_weeks_ago_sunday = date - timedelta(days=days_to_two_weeks_ago_sunday)
    return two_weeks_ago_sunday


def run_rendimientos_descarga_excel(usuario, clave):
    try:
        # # create webdriver object
        options = FirefoxOptions()
        options.headless = False # Set to False if you want to see the browser UI
        driver = webdriver.Remote(command_executor='http://172.17.0.2:4444', options=options)
  
        # # get google.co.in
        driver.get("http://192.168.100.183:18001/sislog/autenticacion/login.do")

        # # Maximize the window and let code stall 
        # # for 10s to properly maximise the window.
        driver.maximize_window()
        time.sleep(2)

        ## 1. AUTHENTICATION
        username = driver.find_element(By.ID, "usuario")
        password = driver.find_element(By.ID, "clave")

        username.send_keys(usuario)
        password.send_keys(clave)

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
        time.sleep(2)

        driver.switch_to.default_content()
        time.sleep(1)

        # 4. SELECT CONTROL
        control = driver.find_element(By.ID, "a_2127-12")
        control.click()
        time.sleep(2)

        # 5. SELECT INFORMES
        informes = driver.find_element(By.ID, "a_2133-12")
        informes.click()
        time.sleep(2)

        # 6. SELECT RENDIMIENTOS
        rendimientos = driver.find_element(By.ID, "a_2136-12")
        rendimientos.click()
        time.sleep(1)

        # 7. SELECT RENDIMIENTOS OPERARIOS
        rendimientos_operatios = driver.find_element(By.ID, "a_2137-12")
        rendimientos_operatios.click()
        time.sleep(1)

        # 8. SELECT RENDIMIENTOS OPERARIOS 2
        rendimientos_operatios_2 = driver.find_element(By.ID, "a_839-12")
        rendimientos_operatios_2.click()
        time.sleep(1)

        ## 9. SELECT DESDE
        desde = driver.find_element(By.ID, "d_fechor_desde")
        desde_hour = get_sunday_two_weeks_ago(datetime.datetime.now())
        desde_day_string = desde_hour.strftime('%d/%m/%Y')
        combine_desde = f"{desde_day_string} 22:00:00"
        print(combine_desde)
        desde.send_keys(combine_desde)


        ## 9. SELECT HASTA
        hasta = driver.find_element(By.ID, "d_fechor_hasta")
        hasta_hour = get_last_sunday(datetime.datetime.now())
        hasta_day_string = hasta_hour.strftime('%d/%m/%Y')
        combine_hasta = f"{hasta_day_string} 22:00:00"
        print(combine_hasta)
        hasta.send_keys(combine_hasta)

        ## 9. SELECT BUSCAR
        time.sleep(2)
        accept_button = driver.find_element(By.XPATH, value="//input[@value='Buscar']")
        accept_button.click()
        print(Fore.LIGHTBLACK_EX,"----")
        print(Fore.CYAN,f"En 10 segundos se descargara como excel")
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(10)


        ## 10. DOWNLOAD EXCEL
        buton_excel = driver.find_element(By.CLASS_NAME, value="export.excel")
        buton_excel.click()
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(1)
        print(Fore.YELLOW,f"Descargando...")
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(10)

        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(1)
        print(Fore.YELLOW,f"Descargado.Puedes cerrar la aplicación o esperar a que se cierre en 30 segundos.")
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(30)

    except Exception as e:
        error_message = str(e)
        if "Failed to decode response from marionette" in error_message:
            driver.quit()