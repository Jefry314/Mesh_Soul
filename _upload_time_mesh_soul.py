# -*- coding: utf-8 -*-

"""
Created on Mon Sep 15 14:32:15 2025

@author: Alvaro.Romero
"""

#%% Imported libraries
import os
import time
import unicodedata
import re
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_FOLDER = r"C:\Users\alvaro.romero\Documents\Proceso_Soul\Horarios"
DOCUMENTS_PATH = BASE_FOLDER
DRIVER_PATH = r"C:\Users\alvaro.romero\Documents\drivers\chromedriver.exe"
LOGIN_LINK = "https://mysoul.groupcos.com/login"
VAR_USER = "Aquinones98"
VAR_PASSWORD = "Mafe031404-+"
MAX_THREADS = 1
MAX_RETRIES = 3
LOG_FOLDER = r"C:\Users\alvaro.romero\Documents\Proceso_Soul"
os.makedirs(LOG_FOLDER, exist_ok=True)

def clean_path(path):
    path = unicodedata.normalize("NFC", path)
    path = path.strip().replace('"', '')
    return os.path.abspath(path)

def wait_for_presence(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

def get_next_week_range():
    today = date.today()
    next_monday = today + timedelta(days=(7 - today.weekday()))
    next_sunday = next_monday + timedelta(days=6)
    return f"Semana del {next_monday:%Y-%m-%d} al {next_sunday:%Y-%m-%d}"

def get_groups_from_folders(base_path):
    groups = []
    if os.path.exists(base_path):
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                groups.append(item)
        print(f"📁 Grupos encontrados: {groups}")
    else:
        print(f"❌ La ruta {base_path} no existe")
    return groups

def get_documents_from_folder(folder_path):
    documents = []
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                valid_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.csv']
                if any(item.lower().endswith(ext) for ext in valid_extensions):
                    documents.append(item_path)
        print(f"📄 Documentos encontrados en {folder_path}: {len(documents)} archivos")
    return documents

class ExportUpload_Soul:
    def __init__(self, driver_path, link, varUser, varPassword):
        self.driver_path = driver_path
        self.link = link
        self.varUser = varUser
        self.varPassword = varPassword
        self.driver = None

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        service = Service(executable_path=self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def login(self):
        if not self.driver:
            self.start_driver()
        print("⏳ Iniciando sesión...")
        self.driver.get(self.link)
        user_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='user']")))
        user_input.clear()
        user_input.send_keys(self.varUser)
        pass_input = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='password']")))
        pass_input.clear()
        pass_input.send_keys(self.varPassword)
        submit_btn = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'][contains(.,'Ingresar')]")))
        submit_btn.click()
        WebDriverWait(self.driver, 20).until(EC.url_contains("https://mysoul.groupcos.com/mios/ciu"))
        self.driver.get("https://mysoul.groupcos.com/mios/ciu/horarios")
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='mat-tab-content-0-0']")))
        print("✅ Login exitoso.")

    def prepare_group_dialog(self, group_name):
        try:
            print(f"⏳ [{group_name}] Abriendo modal...")

            btn_new_conf_xpath = '//*[@id="mat-tab-content-0-0"]/div/div/div[1]/div/div[2]/button[1]'
            button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, btn_new_conf_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(0.5)
            button.click()

            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//mat-option")))

            semana_label = get_next_week_range()
            semana_xpath = f"//mat-option//span[contains(text(),'{semana_label}')]"
            semana_option = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, semana_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", semana_option)
            time.sleep(0.3)
            semana_option.click()
            print(f"✅ Semana configurada: {semana_label}")

            group_input_xpath = '//*[@id="mat-input-5"]'
            group_input = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, group_input_xpath)))
            group_input.clear()
            group_input.send_keys(group_name)
            time.sleep(0.5)

            option_xpath = f'//mat-option//span[normalize-space()="{group_name}"]'
            group_option = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", group_option)
            time.sleep(0.3)
            group_option.click()
            print(f"✅ Grupo {group_name} seleccionado")

            buscar_button_xpath = '//*[@id="mat-dialog-0"]/app-config-schedules/form/mat-dialog-content/div[1]/div/button'
            buscar_button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, buscar_button_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", buscar_button)
            time.sleep(0.3)
            buscar_button.click()
            print("🔎 Botón Buscar presionado correctamente")
            time.sleep(1)

            guardar_button_xpath = '//*[@id="mat-dialog-0"]/app-config-schedules/form/mat-dialog-actions/button[1]'
            guardar_button = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, guardar_button_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", guardar_button)
            time.sleep(0.3)
            guardar_button.click()
            print("💾 Botón Guardar presionado correctamente")
            time.sleep(2)

            return True

        except Exception as e:
            print(f"❌ [{group_name}] Error al preparar modal: {e}")
            return False

    def upload_single_document(self, document_path, group_name):
        document_path = clean_path(document_path)
        if not os.path.isfile(document_path):
            return None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"📤 [{group_name}] Subiendo {os.path.basename(document_path)} (Intento {attempt})...")
                file_input_xpath = '/html/body/div[2]/div[2]/div/mat-dialog-container/app-config-schedules/form/mat-dialog-content/div[2]/div[2]/input'
                file_input = wait_for_presence(self.driver, file_input_xpath, 15)
                if not file_input.is_displayed():
                    self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
                file_input.send_keys(document_path)
                try:
                    boton_si = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[3]/button[1]")))
                    boton_si.click()
                except:
                    file_input.send_keys(Keys.ENTER)

                WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, "//div[contains(.,'Archivo cargado') or contains(.,'Proceso realizado')]")))

                try:
                    boton_aceptar = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button/span[contains(text(),'Aceptar')]/..")))
                    boton_aceptar.click()
                    time.sleep(1)
                except:
                    pass

                print(f"✅ [{group_name}] {os.path.basename(document_path)} subido correctamente.")
                return True

            except Exception as e:
                print(f"⚠️ [{group_name}] Error al subir {os.path.basename(document_path)}: {e}")
                if attempt == MAX_RETRIES:
                    with open(os.path.join(LOG_FOLDER, "documentos_fallidos.log"), "a", encoding="utf-8") as f:
                        f.write(f"{group_name} → {os.path.basename(document_path)} falló tras {MAX_RETRIES} intentos\n")
                    return False

    def process_group(self, group_name, documents_path):
        result = {'group': group_name, 'success': False, 'skipped': [], 'failed': False}
        documents = get_documents_from_folder(os.path.join(documents_path, group_name))
        if not documents:
            result['failed'] = True
            return result
        try:
            self.start_driver()
            self.login()
            if not self.prepare_group_dialog(group_name):
                result['failed'] = True
                with open(os.path.join(LOG_FOLDER, "grupos_fallidos.log"), "a", encoding="utf-8") as f:
                    f.write(f"{group_name} → Error al preparar modal\n")
                return result
            for doc in documents:
                res = self.upload_single_document(doc, group_name)
                if res is None:
                    result['skipped'].append(os.path.basename(doc))
                elif res is False:
                    result['failed'] = True
                    with open(os.path.join(LOG_FOLDER, "grupos_fallidos.log"), "a", encoding="utf-8") as f:
                        f.write(f"{group_name} → {os.path.basename(doc)} no pudo subirse\n")
                    break
            if not result['failed']:
                result['success'] = True
        finally:
            self.close()
        return result

    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    groups = get_groups_from_folders(DOCUMENTS_PATH)
    results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_group = {}
        for group in groups:
            bot = ExportUpload_Soul(DRIVER_PATH, LOGIN_LINK, VAR_USER, VAR_PASSWORD)
            future = executor.submit(bot.process_group, group, DOCUMENTS_PATH)
            future_to_group[future] = group
        for future in as_completed(future_to_group):
            result = future.result()
            results.append(result)

    successful_groups = [r['group'] for r in results if r['success']]
    failed_groups = [r['group'] for r in results if r['failed']]
    skipped_files = [f"{r['group']}/{f}" for r in results for f in r['skipped']]

    print("\n" + "="*50)
    print("📊 RESUMEN DEL PROCESAMIENTO")
    print("="*50)
    print(f"✅ Grupos exitosos ({len(successful_groups)}): {successful_groups}")
    print(f"❌ Grupos fallidos ({len(failed_groups)}): {failed_groups}")
    print(f"⚠️ Archivos omitidos ({len(skipped_files)}): {skipped_files}")
    total = len(successful_groups) + len(failed_groups)
    tasa = (len(successful_groups) / total) * 100 if total else 0
    print(f"📈 Tasa de éxito: {len(successful_groups)}/{total} ({tasa:.1f}%)")

if __name__ == "__main__":
    main()