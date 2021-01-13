import IPy
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Router:
    def __init__(self, ROUTER_HTTP, ROUTER_USERNAME, ROUTER_PASSWORD):
        webdriver_options = webdriver.ChromeOptions()
        webdriver_options.add_argument('--headless')
        webdriver_options.add_argument('disable-infobars')
        webdriver_options.add_argument("--disable-extensions")
        webdriver_options.add_argument("--disable-gpu")
        webdriver_options.add_argument("--disable-dev-shm-usage")
        webdriver_options.add_argument("--no-sandbox")
        webdriver_options.add_argument("--window-size=1024,768")
            
        self.driver = webdriver.Chrome(options=webdriver_options)
        self.driver.set_window_size(1024, 768)
        self.driver.set_window_position(0, 0)
        self.driver.get(ROUTER_HTTP)

        self.ROUTER_USERNAME = ROUTER_USERNAME
        self.ROUTER_PASSWORD = ROUTER_PASSWORD

        self.timeout_sleep = 3

    def login(self):
        self.driver.switch_to.default_content()

        self.driver.find_element_by_id("txt_Username").send_keys(self.ROUTER_USERNAME)
        self.driver.find_element_by_id("txt_Password").send_keys(self.ROUTER_PASSWORD)

        self.driver.find_element_by_id("button").click()

        sleep(self.timeout_sleep)

    def logout(self):
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="headerLogoutText"]').click()

        sleep(self.timeout_sleep)

    def switch_wan_enabled(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "wanInstTable_tbl"))
        )
        self.driver.find_element_by_xpath('//*[@id="wanInstTable_1_1"]').click()
        self.driver.find_element_by_xpath('//*[@id="WanSwitch"]').click()
        actionButton = self.driver.find_element_by_id('ButtonApply')

        self.driver.execute_script("arguments[0].scrollIntoView();", actionButton)
        actionButton.click()

        sleep(self.timeout_sleep)

    def restart_wan(self):
        self.driver.switch_to.default_content()

        self.driver.find_element_by_css_selector('div[name="maindiv_wan"]').click()
        self.driver.switch_to.frame(self.driver.find_element_by_id("frameContent"))

        self.switch_wan_enabled()
        
        self.switch_wan_enabled()
            
        sleep(self.timeout_sleep)


    def get_current_ip(self):
        self.driver.switch_to.default_content()

        self.driver.find_element_by_css_selector('div[name="maindiv_waninfo"]').click()

        self.driver.find_element_by_css_selector('div[name="subdiv_waninfo"]').click()

        self.driver.switch_to.frame(self.driver.find_element_by_id("frameContent"))

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "IPTable"))
        )

        return IPy.IP(self.driver.find_element_by_xpath('//*[@id="record_1"]/td[3]').text)

    def __del__(self):
        self.driver.close()
