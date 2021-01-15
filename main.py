import os
import sys
import IPy
import timeit
from time import sleep
from datetime import datetime
from library.router import Router
from library.cloudflare import Cloudflare
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def main():
    router = Router(
        os.getenv("ROUTER_HTTP"), os.getenv("ROUTER_USERNAME"), os.getenv("ROUTER_PASSWORD"))
    
    router.login()
    print(str(datetime.now()) + " | Login Router Success")

    if len(sys.argv) > 1 and sys.argv[1] == "restart":
        print(str(datetime.now()) + " | Restart WAN for Reset IP")
        router.restart_wan()

    ip = IPy.IP(router.get_current_ip())
    print(str(datetime.now()) + " | IP " + str(ip))

    i = 1
    while ip.iptype() == "PRIVATE":
        print(str(datetime.now()) + " | Restart WAN Attempt " + str(i))
        router.restart_wan()
        
        ip = IPy.IP(router.get_current_ip())
        print(str(datetime.now()) + " | IP " + str(ip))

        i = i + 1

    router.logout()
    print(str(datetime.now()) + " | Logout Router Success")

    del router

    cloudflare = Cloudflare(
            os.getenv("CF_EMAIL"), 
            os.getenv("CF_API_KEY"), 
            os.getenv("CF_ZONE_ID"), 
            os.getenv("CF_RECORD_ID"), 
            os.getenv("CF_DOMAIN_NAME"), 
            os.getenv("CF_PROXIED")
        )

    if str(ip) != cloudflare.get_current_ip()['ip']:
        cloudflare.change_domain_ip(str(ip))
        print(str(datetime.now()) + " | Success Changed Domain IP")
    else:
        print(str(datetime.now()) + " | Domain IP Same")
        
    print(str(datetime.now()) + " | IP " + str(ip))
    
if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(str(datetime.now()) + " | Runtime : " + str(stop - start) + " seconds")