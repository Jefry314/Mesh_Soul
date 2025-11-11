# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 15:13:03 2025

@author: Alvaro.Romero
"""
#%% Imported libraries

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_and_click(driver, xpath, timeout=10):
    """
    Espera que un elemento sea clickeable y hace click.
    """
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()
    return element


def wait_and_type(driver, xpath, text, timeout=10, clear_first=True):
    """
    Espera un input y escribe texto.
    clear_first=True limpia el campo antes de escribir.
    """
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    if clear_first:
        element.clear()
    element.send_keys(text)
    return element


def wait_for_presence(driver, xpath, timeout=10):
    """
    Espera que un elemento exista en el DOM (aunque no sea visible).
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def wait_for_visibility(driver, xpath, timeout=10):
    """
    Espera que un elemento sea visible en pantalla.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def wait_for_url_contains(driver, text, timeout=10):
    """
    Espera que la URL actual contenga un texto específico.
    """
    WebDriverWait(driver, timeout).until(EC.url_contains(text))
    return driver.current_url
