#!/bin/python

import argparse
import sqlite3
try:
    import json
except ImportError:
    import simplejson as json

dbname = 'cmdb.db'

class CMDBInventory(object):
    def __init__(self):
        self.cur = None
        self.inventory = dict()
        
        self.parse_cli_args()
        try:
            con = sqlite3.connect(dbname)
            self.cur = con.cursor()
        except:
            raise

        # Data to print
        if self.args.host:
            data_to_print = self.get_host_info()
        elif self.args.list:
            # Display list of instances for inventory
            self.load_inventory()
            data_to_print = self.json_format_dict(self.inventory, True)
        else:
            # default action with no options
            self.load_inventory()
            data_to_print = self.json_format_dict(self.inventory, True)

        print(data_to_print)

    def parse_cli_args(self):
        """ Command line argument processing """

        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory file based on a CMDB')
        parser.add_argument('--list', action='store_true', default=True, help='List hosts (default: True)')
        parser.add_argument('--host', action='store', help='Get all the variables about a specific hosts')

        self.args = parser.parse_args()

    def get_host_info(self):
        """ Get variables about a specific host from CMDB """
        try:
            self.cur.execute("SELECT host,ip_provision,ansible_ssh_user FROM inventory WHERE host='%s'" % self.args.host)   
            host_data = self.cur.fetchone()
            self.inventory[host_data[0]] = dict()
            self.inventory[host_data[0]]["ansible_ssh_host"] = host_data[1]
            self.inventory[host_data[0]]["ansible_ssh_user"] = host_data[2]
        except:
            pass
        return self.json_format_dict(self.inventory, True)

    def load_inventory(self):
        """ Load entire inventory from CMDB """
        try:
            self.cur.execute("SELECT host,ip_provision,ansible_ssh_user FROM inventory")   
            for row in self.cur:
                self.inventory[row[0]] = dict()
                self.inventory[row[0]]["ansible_ssh_host"] = row[1]
                self.inventory[row[0]]["ansible_ssh_user"] = row[2]
        except:
            raise
            pass

    def json_format_dict(self, data, pretty=False):
        """ Converts a dict to a JSON object and dumps it as a formatted string """

        if pretty:
            return json.dumps(data, sort_keys=True, indent=2)
        else:
            return json.dumps(data)


CMDBInventory()