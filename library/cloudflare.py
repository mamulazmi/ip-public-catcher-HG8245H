import sys
import json
import requests
from IPy import IP

class Cloudflare:
    def __init__(self, CF_EMAIL, CF_API_KEY, CF_ZONE_ID, CF_RECORD_ID, CF_DOMAIN_NAME, CF_PROXIED = True):
        self.CF_EMAIL = CF_EMAIL
        self.CF_API_KEY = CF_API_KEY

        self.CF_ZONE_ID = CF_ZONE_ID
        self.CF_RECORD_ID = CF_RECORD_ID
        self.CF_DOMAIN_NAME = CF_DOMAIN_NAME
        self.CF_PROXIED = CF_PROXIED


    def get_current_ip(self):

        resp = self.request(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
                self.CF_ZONE_ID, self.CF_RECORD_ID),
            'get',
            {}
        )

        return {
            'ip': resp.json()["result"]["content"],
            'type': IP(resp.json()["result"]["content"]).iptype()
        }

    def change_domain_ip(self, ip):
        self.request(
            'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
                self.CF_ZONE_ID, self.CF_RECORD_ID),
            'put',
            {
                'type': 'A',
                'name': self.CF_DOMAIN_NAME,
                'content': ip,
                'proxied': bool(self.CF_PROXIED)
            }
        )

        return True

    def request(self, url, method, json):
        return requests.request(
            url=url, 
            method=method, 
            json=json, 
            headers={
                'X-Auth-Key': self.CF_API_KEY,
                'X-Auth-Email': self.CF_EMAIL
            }
        )