from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas

from driver import Driver

class Liepin(Driver):
    
    def __init__(self, date: str):
        super(Liepin, self).__init__()
        self.url = 'https://www.liepin.com/zhaopin/?city=060020&dq=060020&pubTime=3&currentPage=0&pageSize=40&key=&suggestTag=&workYearCode=0&compId=&compName=&compTag=&industry=&salary=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&sfrom=search_job_pc&ckId=sy7ijqdszgh3gz723gist323c0ok1yqa&skId=vr6xsnw3pwbtp7ddavp6lhix5eg0oiy8&fkId=sy7ijqdszgh3gz723gist323c0ok1yqa&scene=condition&suggestId='
        self.date = date
    
    def per_get(self, url :str, search_key :str):
        self.driver.get(url)
        
        sleep(3) 
        key_input = self.driver.find_element(By.XPATH, "//*[@class='jsx-1374046090']")
        key_input.send_keys(Keys.CONTROL, 'a')
        key_input.send_keys(search_key, Keys.ENTER)
        self.driver.find_element(By.XPATH, "//*[@class='jsx-1374046090 search-btn']").click()

    def page_get(self, job_infos: list):
        joblist_items = self.driver.find_elements(By.XPATH, "//*[@class='jsx-2297469327 job-card-pc-container']")
        self.original_handle = self.driver.current_window_handle
         
        for job_item in joblist_items:
            job = job_item.find_element(By.XPATH, "./div[1]/div/a")

            try:
                title = job.find_element(By.XPATH, "./div[1]/div/div[1]").text
            except:
                title = ''
            try:
                salary = job.find_element(By.XPATH, "./div[1]/span").text
            except:
                salary = ''

            try:
                company = job_item.find_element(By.XPATH, './div[1]/div/div/div/span').text
            except:
                company = ''

            try:
                location = job.find_element(By.XPATH, './div[1]/div/div[2]/span[2]').text
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
            res['工作信息'] = self.driver.find_element(By.XPATH, "/html/body/main/content/section[2]/dl/dd").text
        except:
            pass
        
        self.driver.close()
        self.driver.switch_to.window(self.original_handle)

    def next_page(self):
        self.driver.find_element(By.XPATH, '//*[@class="anticon anticon-right"]').click()
        

    def data_to_excel(self, job_infos: list, search_key :str):
        file_name = f"{self.date}\\liepin-{search_key}.xlsx"
        
        pd = pandas.DataFrame(job_infos, columns=['职位名称', '发布时间','薪水', '地点', '公司名称','工作信息','链接'])
        pd.to_excel(file_name)

        


