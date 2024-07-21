from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import List


class WebDriverSetup:
    @staticmethod
    def setup_driver() -> webdriver.Chrome:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)


class MateTeeLinkFetcher:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def fetch_links(self, base_url: str) -> List[str]:
        self.driver.get(base_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[filters-module="product-name"]')
            )
        )
        product_names = self.driver.find_elements(
            By.CSS_SELECTOR, '[filters-module="product-name"]'
        )
        unique_links = {
            product_name.find_element(By.XPATH, "..").get_attribute("href")
            for product_name in product_names
            if product_name.find_element(By.XPATH, "..").get_attribute("href")
        }
        return list(unique_links)
