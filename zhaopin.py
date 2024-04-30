from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas

from driver import Driver

class Zhaopin(Driver):
    
    def __init__(self, date: str):
        super(Zhaopin, self).__init__()
        self.url = 'https://sou.zhaopin.com/?jl=635'
        self.date = date
        self.index = 0
        self.current_key = ''
    
    def per_get(self, url :str, search_key :str):
        self.driver.get(url)
        
        sleep(3) 
        key_input = self.driver.find_element(By.XPATH, "//*[@class='query-search__content-input']")
        key_input.send_keys(Keys.CONTROL, 'a')
        key_input.send_keys(search_key, Keys.ENTER)
        self.driver.find_element(By.XPATH, "//*[@class='query-search__content-button']").click()
        self.driver.find_element(By.XPATH, "//*[@class='listsort__item__a' and contains(text(), '最新发布')]").click()
        self.index = 1
        self.current_key = search_key

    def page_get(self, job_infos: list):
        if self.index != 1:
            url = self.driver.current_url[:-1] + str(self.index)
            self.driver.get(url)

        joblist_items = self.driver.find_elements(By.XPATH, "//*[@class='joblist-box__item clearfix']")
        self.original_handle = self.driver.current_window_handle

        for job_item in joblist_items:
            job = job_item.find_element(By.XPATH, "./div[1]/div[1]/div[1]/a")

            try:
                salary = job_item.find_element(By.XPATH, "./div[1]/div[1]/div[1]/p").text
            except:
                salary = ''
            try:
                company = job_item.find_element(By.XPATH, './div[1]/div[2]/div[1]/a').text
            except:
                company = ''
            try:
                location = job_item.find_element(By.XPATH, './div[1]/div[1]/div[3]/div[1]/span').text
            except:
                location = ''
            res = {
                '职位名称': job.text,
                '发布时间': '',
                '薪水': salary,
                '工作信息': '',
                '公司名称': company,
                '地点': location,
                '链接': job.get_attribute('href')
            }

            self.subpage_get(res, job.get_attribute('href'))
            print(res)
            
            job_infos.append(res)

    def subpage_get(self, res:dict, url:str):
        self.driver.execute_script(f'window.open("{url}")')
        for win_handle in self.driver.window_handles:
            if win_handle != self.original_handle:
                self.driver.switch_to.window(win_handle)

        sleep(1)
        try:
            res['工作信息'] = self.driver.find_element(By.XPATH, "//*[@class='describtion__detail-content']").text
        except:
            pass
        
        self.driver.close()
        self.driver.switch_to.window(self.original_handle)

    def next_page(self):
        self.index += 1

    def data_to_excel(self, job_infos: list, search_key :str):
        file_name = f"{self.date}\\zhaopin-{search_key}.xlsx"
        
        pd = pandas.DataFrame(job_infos, columns=['职位名称', '发布时间','薪水', '地点', '公司名称','工作信息','链接'])
        pd.to_excel(file_name)

        


