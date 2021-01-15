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
        prefs = {'profile.default_content_setting_values': {'cookies': 0, 'images': 2, 'javascript': 0, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2}}
        webdriver_options.add_experimental_option('prefs', prefs)
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
        
        self.ROUTER_HTTP = ROUTER_HTTP
        self.ROUTER_USERNAME = ROUTER_USERNAME
        self.ROUTER_PASSWORD = ROUTER_PASSWORD

        self.timeout_sleep = 2

    def login(self):
        self.driver.get(self.ROUTER_HTTP)

        self.driver.find_element_by_id("txt_Username").send_keys(self.ROUTER_USERNAME)
        self.driver.find_element_by_id("txt_Password").send_keys(self.ROUTER_PASSWORD)

        self.driver.find_element_by_id("button").click()

        sleep(self.timeout_sleep)

    def logout(self):
        
        self.driver.get(
            self.ROUTER_HTTP + '/index.asp'
        )
        
        self.driver.find_element_by_id('headerLogoutText').click()

        sleep(self.timeout_sleep)

    def switch_wan_enabled(self):

        self.driver.get(
            self.ROUTER_HTTP + '/html/bbsp/wan/wan.asp'
        )

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "wanInstTable_tbl"))
        )
        self.driver.find_element_by_id('wanInstTable_1_1').click()
        self.driver.find_element_by_id('WanSwitch').click()
        actionButton = self.driver.find_element_by_id('ButtonApply')

        self.driver.execute_script("arguments[0].scrollIntoView();", actionButton)
        actionButton.click()

        sleep(self.timeout_sleep)

    def restart_wan(self):

        self.switch_wan_enabled()
        
        self.switch_wan_enabled()
            
        sleep(self.timeout_sleep)


    def get_current_ip(self):
        
        self.driver.get(
            self.ROUTER_HTTP + '/html/bbsp/waninfo/waninfo.asp'
        )

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "IPTable"))
        )

        return IPy.IP(self.driver.find_element_by_css_selector('#record_1 > td:nth-child(3)').text)

    def __del__(self):
        self.driver.close()
