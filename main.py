import sys
import IPy
import env
import cloudflare
import router_selenium
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def main():
    driver = webdriver.Remote(
        command_executor=env.WEBDRIVER_URL, 
        desired_capabilities=DesiredCapabilities.FIREFOX    
    )
    driver.set_window_size(1024, 768)

    print(str(datetime.now()) + " | Try Connecting To Web Driver")
    driver.get(env.ROUTER_IP)
    
    router_selenium.login(driver)
    print(str(datetime.now()) + " | Login Router Success")


    print(str(datetime.now()) + " | Get Current IP Process")
    ip = IPy.IP(router_selenium.get_current_ip(driver))
    print(str(datetime.now()) + " | Current IP " + str(ip))


    if len(sys.argv) > 1 and sys.argv[1] == "restart":
        print(str(datetime.now()) + " | Restart WAN for Reset IP")
        router_selenium.restart_wan(driver)

    i = 1
    while ip.iptype() == "PRIVATE":

        router_selenium.restart_wan(driver)
        print(str(datetime.now()) + " | Restart WAN Attempt " + str(i))

        ip = IPy.IP(router_selenium.get_current_ip(driver))
        print(str(datetime.now()) + " | Current IP " + str(ip) + " Attempt " + str(i))

        i = i + 1

    router_selenium.logout(driver)
    print(str(datetime.now()) + " | Logout Router Success")

    driver.close()

    print(str(datetime.now()) + " | Get Cloudflare Current IP Process")
    cloudflareCurrentIp = cloudflare.get_current_ip()

    if str(ip) != cloudflareCurrentIp['ip']:
        cloudflare.change_domain_ip(str(ip))
        print(str(datetime.now()) + " | Success Changed Domain IP")
    else:
        print(str(datetime.now()) + " | Domain IP Same")
        
    print(str(datetime.now()) + " | Current IP " + str(ip))
    
if __name__ == "__main__":
    print(" =================================== ")
    main()