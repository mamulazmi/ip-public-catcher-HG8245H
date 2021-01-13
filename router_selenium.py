import env
import IPy
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    driver.switch_to.default_content()

    driver.find_element_by_id("txt_Username").send_keys(env.ROUTER_USERNAME)
    driver.find_element_by_id("txt_Password").send_keys(env.ROUTER_PASSWORD)

    driver.find_element_by_id("button").click()

    time.sleep(2)

def logout(driver):
    driver.switch_to.default_content()
    driver.find_element_by_xpath('//*[@id="headerLogoutText"]').click()

def restart_wan(driver):
    driver.switch_to.default_content()

    driver.find_element_by_css_selector('div[name="maindiv_wan"]').click()
    driver.switch_to.frame(driver.find_element_by_id("frameContent"))

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "wanInstTable_tbl"))
    )
    driver.find_element_by_xpath('//*[@id="wanInstTable_1_1"]').click()
    driver.find_element_by_xpath('//*[@id="WanSwitch"]').click()
    driver.find_element_by_xpath('//*[@id="ButtonApply"]').click()

    time.sleep(3)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "wanInstTable_tbl"))
    )
    driver.find_element_by_xpath('//*[@id="wanInstTable_1_1"]').click()
    driver.find_element_by_xpath('//*[@id="WanSwitch"]').click()
    driver.find_element_by_xpath('//*[@id="ButtonApply"]').click()

    time.sleep(3)

def get_current_ip(driver):
    driver.switch_to.default_content()

    driver.find_element_by_css_selector('div[name="maindiv_waninfo"]').click()

    driver.find_element_by_css_selector('div[name="subdiv_waninfo"]').click()

    driver.switch_to.frame(driver.find_element_by_id("frameContent"))

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "IPTable"))
    )

    return driver.find_element_by_xpath('//*[@id="record_1"]/td[3]').text
