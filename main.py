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
    start = timeit.default_timer()

    router = Router(
        os.getenv("ROUTER_HTTP"), 
        os.getenv("ROUTER_USERNAME"), 
        os.getenv("ROUTER_PASSWORD")
    )
    
    router.login()
    print(str(datetime.now()) + " | Login Router Success")

    oldIp = ip = IPy.IP(router.get_current_ip())
    print(str(datetime.now()) + " | Current IP : " + str(ip))

    restart = (len(sys.argv) > 1 and sys.argv[1] == "restart")
    
    i = 1       
    while (ip.iptype() == "PRIVATE" or restart):
        router.restart_wan()

        ip = IPy.IP(router.get_current_ip())
        print(str(datetime.now()) + " | Restart WAN #" + str(i) + " Attempt | Obtain IP : " + str(ip))

        restart = False
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
        
    print(str(datetime.now()) + " | Old IP " + str(oldIp))
    print(str(datetime.now()) + " | New IP " + str(ip))

    stop = timeit.default_timer()
    print(str(datetime.now()) + " | Runtime : " + str(round(stop - start, 2)) + " seconds")

if __name__ == "__main__":
    main()