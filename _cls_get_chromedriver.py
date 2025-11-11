# -*- coding: utf-8 -*-
"""
@author: Alvaro.Romero
"""

import os
import re
import requests
import zipfile
import subprocess
import shutil
import win32api
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

DRIVER_DIR = Path(r"C:\Users\alvaro.romero\Documents\drivers")
DRIVER_DIR.mkdir(exist_ok=True)
DRIVER_PATH = DRIVER_DIR / "chromedriver.exe"


def get_chrome_version():
    """Obtiene la versión de Google Chrome leyendo la info del ejecutable."""
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        try:
            info = win32api.GetFileVersionInfo(chrome_path, "\\")
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
            return version
        except Exception as e:
            print("❌ No pude obtener la versión desde propiedades del archivo:", e)
    return None

def download_chromedriver(version):
    """Descarga la versión de ChromeDriver que corresponde al Chrome detectado."""
    major_version = version.split(".")[0]
    print(f"🌐 Detectando ChromeDriver para versión {major_version}...")

    url_last = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{major_version}"
    latest_version = requests.get(url_last).text.strip()

    print(f"📥 Última versión disponible: {latest_version}")

    zip_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{latest_version}/win32/chromedriver-win32.zip"
    zip_path = DRIVER_DIR / "chromedriver.zip"

    with requests.get(zip_url, stream=True) as r:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        if DRIVER_PATH.exists():
            DRIVER_PATH.unlink()
        zip_ref.extract("chromedriver-win32/chromedriver.exe", DRIVER_DIR)
        extracted = DRIVER_DIR / "chromedriver-win32" / "chromedriver.exe"
        shutil.move(str(extracted), DRIVER_PATH)
        shutil.rmtree(DRIVER_DIR / "chromedriver-win32", ignore_errors=True)

    os.remove(zip_path)
    print(f"✅ ChromeDriver actualizado en: {DRIVER_PATH}")
    return DRIVER_PATH

if __name__ == "__main__":
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("⚠️ No se pudo detectar Chrome, verifica que esté instalado.")
    else:
        print(f"🔍 Versión de Chrome detectada: {chrome_version}")
        driver_path = download_chromedriver(chrome_version)
        chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        chrome_options = Options()
        chrome_options.binary_location = chrome_path

        service = Service(str(driver_path))
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get("https://www.google.com")
        print("🌐 Chrome abierto en Google.com")