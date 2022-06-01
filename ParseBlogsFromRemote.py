import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

REMOTE_URL = ""
cromeDriverPath = "/Users/raquelfreire/Documents/chromedriver"
arrayOfCategories = ["https://volan.app.br/category/controle-de-processos/page/2/",
                     "https://volan.app.br/category/gestao-administrativa-e-financeira/page/2/",
                     "https://volan.app.br/category/gestao-de-empresas-medicas/page/2/",
                     "https://volan.app.br/category/gestao-de-empresas-medicas/page/3/",
                     "https://volan.app.br/category/gestao-de-empresas-medicas/page/4/",
                     "https://volan.app.br/category/gestao-de-qualidade/page/2/"]

if __name__ == '__main__':

    for category in arrayOfCategories:
        s = Service(cromeDriverPath)
        driver = webdriver.Chrome(service=s)
        driver.get(category)
        time.sleep(3)

        for btn in driver.find_elements(by=By.CLASS_NAME, value="more-link"):
            innerS = Service(cromeDriverPath)
            innerDriver = webdriver.Chrome(service=innerS)
            innerDriver.get(btn.get_attribute("href"))
            time.sleep(3)
            pyautogui.hotkey('command', 's')
            time.sleep(1)
            pyautogui.press('enter')
            # esperar baixar
            time.sleep(10)

            innerDriver.quit()

        driver.quit()
