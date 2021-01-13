import env
import sys
import json
import requests
from IPy import IP

def get_current_ip():
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            env.CF_ZONE_ID, env.CF_RECORD_ID),
        headers={
            'X-Auth-Key': env.CF_API_KEY,
            'X-Auth-Email': env.CF_EMAIL
        })

    return {
        'ip': resp.json()["result"]["content"],
        'type': IP(resp.json()["result"]["content"]).iptype()
    }

def change_domain_ip(ip):
    requests.put(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
            env.CF_ZONE_ID, env.CF_RECORD_ID),
        json={
            'type': 'A',
            'name': env.CF_DOMAIN_NAME,
            'content': ip,
            'proxied': env.CF_PROXIED
        },
        headers={
            'X-Auth-Key': env.CF_API_KEY,
            'X-Auth-Email': env.CF_EMAIL
        })

    return True