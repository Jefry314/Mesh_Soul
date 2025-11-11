# -*- coding: utf-8 -*-
"""
Helper para automatización con Selenium y Chrome
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC


class WebScraping_Chrome:

    @staticmethod
    def Webdriver_ChrDP(driver_path):

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    @staticmethod
    def Webdriver_ChrDP_DP(driver_path, download_path):
        """Chrome con ruta de descargas personalizada"""
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        prefs = {"download.default_directory": download_path}
        options.add_experimental_option("prefs", prefs)

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    @staticmethod
    def Webdriver_ChrPP_DP(profile_path, driver_path):
        """Chrome usando un perfil de usuario existente"""
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-data-dir={profile_path}")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    # ----------------------------
    # Helpers para acciones comunes
    # ----------------------------
    @staticmethod
    def WebScraping_Acces(driver, link):
        driver.get(link)

    @staticmethod
    def WebScraping_Keys(driver, xpath_, s_keys):
        keys = driver.find_element(By.XPATH, xpath_)
        keys.send_keys(s_keys)

    @staticmethod
    def WebScraping_KeysCSS(driver, css_, s_keys):
        keys = driver.find_element(By.CSS_SELECTOR, css_)
        keys.send_keys(s_keys)

    @staticmethod
    def WebScraping_Nav(driver, xpath_):
        button = driver.find_element(By.XPATH, xpath_)
        button.click()

    @staticmethod
    def WebScraping_NavCSS(driver, css_):
        button = driver.find_element(By.CSS_SELECTOR, css_)
        button.click()

    @staticmethod
    def WebScraping_Wait(driver, wait, xpath_):
        WebDriverWait(driver, wait).until(
            EC.presence_of_element_located((By.XPATH, xpath_))
        )

    @staticmethod
    def WebScraping_Select(driver, name_id, text):
        source = driver.find_element(By.NAME, name_id)
        source_select = Select(source)
        source_select.select_by_visible_text(text)