import telnetlib
import re

class Telnet:
    def __init__(self, HOST, USERNAME, PASSWORD):
        self.telnet = telnetlib.Telnet(HOST)
        
        self.telnet.read_until(b"Login:")
        self.telnet.write(str(USERNAME + "\n").encode('utf-8'))

        self.telnet.read_until(b"Password:")
        self.telnet.write(str(PASSWORD + "\n").encode('utf-8'))


    def get_current_ip(self):
        self.telnet.read_until(b"WAP>")
        self.telnet.write(b"display pppoe client all\n")

        raw = str(self.telnet.read_until(b"WAP>"))

        ip =  re.findall( r'[0-9]+(?:\.[0-9]+){3}', raw)[0]

        self.telnet.write(str("\n").encode('utf-8'))

        return ip


    def logout(self):
        self.telnet.read_until(b"WAP>")

        self.telnet.write(b"logout\n")