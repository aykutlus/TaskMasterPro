
# import webdriver
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
from datetime import datetime, timedelta
import datetime
from selenium.webdriver.common.keys import Keys

from datetime import datetime, timedelta
from selenium.webdriver.firefox.options import Options as FirefoxOptions



def get_date_range():
    today = datetime.today()
    if today.weekday() == 0:  # If today is Monday
        since_date = today - timedelta(days=3)  # Previous Friday
        until_date = today - timedelta(days=1)  # Previous Saturday
    else:
        since_date = today - timedelta(days=1)
        until_date = since_date

    since_date_str = since_date.strftime('%d/%m/%Y')
    until_date_str = until_date.strftime('%d/%m/%Y')

    return since_date_str, until_date_str

def run_devolucion_tienda(usuario, clave):

    try:
        # Example usage:
        since_date, until_date = get_date_range()

        # # create webdriver object
        options = FirefoxOptions()
        options.headless = False # Set to False if you want to see the browser UI
        driver = webdriver.Remote(command_executor='http://172.17.0.2:4444', options=options)  
              
        # # get google.co.in
        driver.get("http://192.168.100.166:8124/auth/login/page")

        # # Maximize the window and let code stall 
        # # for 10s to properly maximise the window.
        driver.maximize_window()
        time.sleep(2)

        ## 1. AUTHENTICATION
        username = driver.find_element(By.ID, "login")
        password = driver.find_element(By.ID, "password")

        username.send_keys(usuario)
        password.send_keys(clave)

        accept_button = driver.find_element(By.ID, "go-basic")
        accept_button.click()


        ## 2. DOWN ICON
        down_icon = None

        while down_icon is None:
            try:
                down_icon = driver.find_element(By.CSS_SELECTOR, ".s_profile_bar_bookmark_dropdown.s_profile_bar_iconlink")
            except Exception:
                pass  # Continue waiting until the element is found

        down_icon.click()


        ## 3. Click Ejecucion de Consultas
        execution = None

        while execution is None:
            try:
                execution = driver.find_element(By.LINK_TEXT, "Ejecución de consultas")
            except Exception:
                pass  # Continue waiting until the element is found

        execution.click()

        ## 4. Click Devolucion de tiendas
        devo = None

        while devo is None:
            try:
                devo = driver.find_element(By.XPATH, "//div[contains(text(), 'ZPVMDEVO')]")
                time.sleep(5)
            except Exception:
                pass  # Continue waiting until the element is found
        devo.click()


        ## 5. Click Criterios
        criterios = None

        while criterios is None:
            try:
                criterios = driver.find_element(By.LINK_TEXT, "Criterios")
                time.sleep(5)
            except Exception:
                pass  # Continue waiting until the element is found
        criterios.click()



        # Example usage:
        since_date, until_date = get_date_range()
        print(f"Since: {since_date}, Until: {until_date}")

        ## 6. Put Desde
        ##the id is different each time. whats common in each login is 58-input. so find a way to get it with ends with.

        # Get all elements on the page
        elements = driver.find_elements(By.XPATH, '//*')

        # List to store element IDs
        extracted_number = None

        # Extract IDs of elements
        for element in elements:
            try:
                element_id = element.get_attribute("id")
                if element_id:
                    for char in element_id:
                        # Check if the character is a digit
                        if char.isdigit():
                            # If a digit is found, extract it, assign it to extracted_number, and break the loop
                            extracted_number = int(char) 
                            break
                    # If a number is found, break the outer loop
                    if extracted_number is not None:
                        break
            except Exception as e:
                print(f"An error occurred: {str(e)}")

        print(extracted_number)

        time.sleep(1)

        desde = None
        while desde is None:
            try:
                desde = driver.find_element(By.ID, f"{extracted_number+1}-58-input")
            except Exception:
                pass  # Continue waiting until the element is found

        desde.click()
        time.sleep(2)
        desde.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
        desde.send_keys(Keys.BACKSPACE)  # Delete the selected text
        time.sleep(2)
        desde.send_keys(since_date)
        print("sent keys for desde")

        # 6. Put Hasta
        hasta = None

        while hasta is None:
            try:
                hasta = driver.find_element(By.ID, f"{extracted_number+1}-61-input")
            except Exception:
                pass  # Continue waiting until the element is found

        time.sleep(2)
        hasta.click()
        time.sleep(2)
        hasta.send_keys(Keys.CONTROL + "a")  # Select all text in the input field
        hasta.send_keys(Keys.BACKSPACE)  # Delete the selected text
        time.sleep(2)
        hasta.send_keys(until_date)
        print("sent keys for hasta")

        ## 7. Click OK
        okbutton = None

        while okbutton is None:
            try:
                okbutton = driver.find_element(By.LINK_TEXT, "OK")
                time.sleep(2)
            except Exception:
                pass  # Continue waiting until the element is found

        okbutton.click()
        print("clicked OK")

        ## 7. Click OK
        moreactions = None

        while moreactions is None:
            try:
                moreactionsbutton = driver.find_element(By.ID, f"showMoreActions-{extracted_number}")
                moreactionsbutton.click()
                moreactions = moreactionsbutton
            except Exception:
                time.sleep(5)
                pass  # Continue waiting until the element is found

        print("clicked moreactions")

        ## 8. Click Export
        export = None

        while export is None:
            try:
                export = driver.find_element(By.LINK_TEXT, "Export.")
                time.sleep(5)
            except Exception:
                pass  # Continue waiting until the element is found
        export.click()
        print("clicked export")
        ## 9. Click OK
        ok = None

        while ok is None:
            try:
                ok = driver.find_element(By.LINK_TEXT, "OK")
                time.sleep(5)
            except Exception:
                pass  # Continue waiting until the element is found
        ok.click()
        print("clicked OK")

        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(1)
        print(Fore.YELLOW,f"Descargando... No cierres la applicacion.")
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(30)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(1)
        print(Fore.YELLOW,f"Descargado.Espere a que se cierre la applicacion en 20 segundos.")
        time.sleep(1)
        print(Fore.LIGHTBLACK_EX,"----")
        time.sleep(20)
        driver.close()

    except Exception as e:
        error_message = str(e)
        if "Failed to decode response from marionette" in error_message:
            driver.quit()