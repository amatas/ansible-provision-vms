#!/bin/python

import os
import time
import sqlite3

dbname = 'cmdb.db'
TIME_FORMAT='%Y-%m-%d %H:%M:%S'

try:
    con = sqlite3.connect(dbname)
    cur = con.cursor()
except:
    pass

def log(host, data):

    if type(data) == dict:
        invocation = data.pop('invocation', None)
        if invocation.get('module_name', None) != 'setup':
            return

    facts = data.get('ansible_facts', None)

    now = time.strftime(TIME_FORMAT, time.localtime())

    try:
        cur.execute("Select * from inventory")
    except sqlite3.OperationalError as error:
        if str(error) == 'no such table: inventory':
            cur.execute('''
                create table inventory (
                   last_successfull_update text,
                   host text primary key,
                   total_mem text,
                   num_vcpus text,
                   arch text,
                   dist text,
                   distvers text,
                   sys text,
                   kernel text,
                   interface text,
                   ip_provision text,
                   ansible_ssh_user text,
                   virt_role text,
                   location text,
                   parent_host text);
                ''')

    try:
        cur.execute("REPLACE INTO inventory (last_successfull_update, host, total_mem, num_vcpus, arch, dist, distvers, sys, kernel, interface, ip_provision, ansible_ssh_user, virt_role ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);",
        (
            now,
            facts.get('ansible_hostname', None),
            facts.get('ansible_memtotal_mb',None),
            facts.get('ansible_processor_vcpus',None),
            facts.get('ansible_architecture', None),
            facts.get('ansible_distribution', None),
            facts.get('ansible_distribution_version', None),
            facts.get('ansible_system', None),
            facts.get('ansible_kernel', None),
            facts.get('ansible_default_ipv4',None).get('interface',None),
            facts.get('ansible_default_ipv4',None).get('address',None),
            facts.get('ansible_user_id', None),
            facts.get('ansible_virtualization_role', None)
        ))
        con.commit()
    except:
        pass

class CallbackModule(object):
    def runner_on_ok(self, host, res):
        log(host, res)

if __name__ == "__main__":
    import json
    data = json.load(open('server-test.json'))
    host = 'test-host'
    log (host, data)