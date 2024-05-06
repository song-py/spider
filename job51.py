from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas
import json

from driver import Driver

class Job51(Driver):
    
    def __init__(self, date: str):
        super(Job51, self).__init__()
        self.url = 'http://search.51job.com'
        self.date = date
    
    def per_get(self, url :str, search_key :str):
        self.driver.get(url)
        sleep(1)
        self.slider_check()
        
        sleep(3)
        key_input = self.driver.find_element(By.ID, "keywordInput")
        key_input.send_keys(Keys.CONTROL, 'a')
        key_input.send_keys(search_key, Keys.ENTER)
        self.driver.find_element(By.XPATH, "//span[contains(text(), '展开选项')]").click()
        self.driver.find_element(By.XPATH, "//*[@class='at' and contains(text(), '发布日期')]").click()
        self.driver.find_element(By.XPATH, "//*[contains(text(), '近三天')]").click()
        self.driver.find_element(By.ID, "search_btn").click()
        self.driver.find_element(By.XPATH, "//span[contains(text(), '最新优先')]").click()

    def page_get(self, job_infos: list):
        joblist_items = self.driver.find_elements(By.XPATH, "//*[@class='joblist-item']")
        self.original_handle = self.driver.current_window_handle

        for job_item in joblist_items:
            job = job_item.find_element(By.XPATH, "./*[@class='joblist-item-job sensors_exposure']")
            job_detail = json.loads(job.get_attribute('sensorsdata'))

            try:
                company = job.find_element(By.XPATH, './div[3]/div[1]/a').text
            except:
                company = ''
            res = {
                '职位名称': job_detail['jobTitle'],
                '发布时间': job_detail['jobTime'],
                '薪水': job_detail['jobSalary'],
                '工作信息': '',
                '公司名称': company,
                '公司信息': '',
                '地点': job_detail['jobArea'],
                '链接': ''
            }

            job.find_element(By.XPATH, './div[1]/span[1]').click()
            sleep(2)
            
            self.subpage_get(res)
            print(res)
            
            job_infos.append(res)

    def subpage_get(self, res:dict):
        for win_handle in self.driver.window_handles:
            if win_handle != self.original_handle:
                self.driver.switch_to.window(win_handle)
        
        self.slider_check()

        res['链接'] = self.driver.current_url
        sleep(1)
        try:
            res['工作信息'] = self.driver.find_element(By.XPATH, "//*[@class='bmsg job_msg inbox']").text
            res['公司信息'] = self.driver.find_element(By.XPATH, "//*[@class='tmsg inbox']").text
        except:
            pass
        
        self.driver.close()
        self.driver.switch_to.window(self.original_handle)

    def next_page(self):
        self.driver.find_element(By.XPATH, '//*[@class="btn-next"]').click()

    def data_to_excel(self, job_infos: list, search_key :str):
        file_name = f"{self.date}\\51job-{search_key}.xlsx"
        
        pd = pandas.DataFrame(job_infos, columns=['职位名称', '发布时间','薪水', '地点', '公司名称','工作信息','公司信息','链接'])
        pd.to_excel(file_name)

        


