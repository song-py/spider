from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas

from driver import Driver

class Boss(Driver):
    
    def __init__(self, date: str):
        super(Boss, self).__init__()
        self.url = 'https://www.zhipin.com/web/geek/job?query=&city=101190100'
        self.date = date
        self.index = 0
        self.current_url = ''
    
    def per_get(self, url :str, search_key :str):
        self.driver.get(url)
        
        sleep(20) 
        key_input = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/input")
        key_input.send_keys(Keys.CONTROL, 'a')
        key_input.send_keys(search_key, Keys.ENTER)
        self.driver.find_element(By.XPATH, "//*[@class='search-btn']").click()
        self.index = 1
        self.current_url = self.driver.current_url

    def page_get(self, job_infos: list):
        if self.index != 1:
            url = self.current_url + '&page=' + str(self.index)
            self.driver.get(url)
            sleep(5)

        joblist_items = self.driver.find_elements(By.XPATH, "//*[@class='job-card-wrapper']")
        self.original_handle = self.driver.current_window_handle

        for job_item in joblist_items:
            job = job_item.find_element(By.XPATH, "./div[1]/a")

            try:
                title = job.find_element(By.XPATH, "./div[1]/span[1]").text
            except:
                title = ''
            try:
                salary = job.find_element(By.XPATH, "./div[2]/span").text
            except:
                salary = ''
            try:
                company = job_item.find_element(By.XPATH, './div[1]/div/div[2]/h3').text
            except:
                company = ''
            try:
                location = job.find_element(By.XPATH, './div[1]/span[2]/span').text
            except:
                location = ''
            res = {
                '职位名称': title,
                '发布时间': '',
                '薪水': salary,
                '工作信息': '',
                '公司名称': company,
                '地点': location,
                '链接': job.get_attribute('href')
            }

            #self.subpage_get(res, job.get_attribute('href'))
            print(res)
            
            job_infos.append(res)

    def subpage_get(self, res:dict, url:str):
        self.driver.execute_script(f'window.open("{url}")')
        for win_handle in self.driver.window_handles:
            if win_handle != self.original_handle:
                self.driver.switch_to.window(win_handle)

        sleep(1)
        try:
            res['工作信息'] = self.driver.find_element(By.XPATH, "//*[@class='job-sec-text']").text
        except:
            pass
        
        self.driver.close()
        self.driver.switch_to.window(self.original_handle)

    def next_page(self):
        self.index += 1

    def data_to_excel(self, job_infos: list, search_key :str):
        file_name = f"{self.date}\\boss-{search_key}.xlsx"
        
        pd = pandas.DataFrame(job_infos, columns=['职位名称', '发布时间','薪水', '地点', '公司名称','工作信息','链接'])
        pd.to_excel(file_name)

        


