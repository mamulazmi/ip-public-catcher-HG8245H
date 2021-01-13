import sys
import IPy
import env
import timeit
import cloudflare
import router_selenium
from time import sleep
from datetime import datetime
from selenium import webdriver

def main():
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('disable-infobars')
    webdriver_options.add_argument("--disable-extensions")
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument("--disable-dev-shm-usage")
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument("--window-size=1024,768")
        
    driver = webdriver.Chrome(options=webdriver_options)
    driver.set_window_size(1024, 768)
    driver.set_window_position(0, 0)

    print(str(datetime.now()) + " | Try Connecting To Web Driver")
    driver.get(env.ROUTER_IP)
    
    router_selenium.login(driver)
    print(str(datetime.now()) + " | Login Router Success")

    if len(sys.argv) > 1 and sys.argv[1] == "restart":
        print(str(datetime.now()) + " | Restart WAN for Reset IP")
        router_selenium.restart_wan(driver)

    ip = IPy.IP(router_selenium.get_current_ip(driver))
    print(str(datetime.now()) + " | Current IP " + str(ip))

    i = 1
    while ip.iptype() == "PRIVATE":
        print(str(datetime.now()) + " | Restart WAN Attempt " + str(i))
        router_selenium.restart_wan(driver)
        
        ip = IPy.IP(router_selenium.get_current_ip(driver))
        print(str(datetime.now()) + " | Current IP " + str(ip))

        i = i + 1

    router_selenium.logout(driver)
    print(str(datetime.now()) + " | Logout Router Success")

    driver.close()

    cloudflareCurrentIp = cloudflare.get_current_ip()

    if str(ip) != cloudflareCurrentIp['ip']:
        cloudflare.change_domain_ip(str(ip))
        print(str(datetime.now()) + " | Success Changed Domain IP")
    else:
        print(str(datetime.now()) + " | Domain IP Same")
        
    print(str(datetime.now()) + " | Current IP " + str(ip))
    
if __name__ == "__main__":
    print(" =================================== ")
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(str(datetime.now()) + " | Runtime : " + str(stop - start))