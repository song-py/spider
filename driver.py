from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import random

class Driver:
    
    def __init__(self, headless: bool = False):
        options = webdriver.ChromeOptions()
        
        # webdriver
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        if headless:
            options.add_argument('--headless')
        
        self.driver = webdriver.Chrome(options)
        self.url = ''

    def slider_check(self):
        try:
            action = ActionChains(self.driver)
            slider_bar = self.driver.find_element(By.ID, "nc_1_n1z")
            action.click_and_hold(slider_bar).perform()
            action.move_by_offset(random.randint(100,200),0).perform()
            sleep(1)
            action.move_by_offset(300,0).perform()
            action.release().perform()
        except:
            pass

    def per_get(self, url :str, search_key :str):
        raise NotImplementedError

    def page_get(self, job_infos: list):
        raise NotImplementedError

    def next_page(self):
        raise NotImplementedError
    
    def data_to_excel(self, job_infos: list, search_key :str):
        raise NotImplementedError
    
    def run(self, keys:list, pages: int):
        for key in keys:
            try:
                self.per_get(self.url, key)
            except Exception as e:
                print(e)
                continue
        
            job_infos = []
            for i in range(pages):
                sleep(1)
                try:
                    self.page_get(job_infos)
                    self.next_page()
                except Exception as e:
                    print(e)
                    continue
            
            self.data_to_excel(job_infos, key)
 
