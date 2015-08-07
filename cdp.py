#!/usr/bin/python3

import os
import sys
import time
import ssl
from suds.client import Client

class cdp(object):

    def __init__(self, soap_host, soap_port, soap_user, soap_pass):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.soap_host = soap_host
        self.soap_port = soap_port
        self.soap_user = soap_user
        self.soap_pass = soap_pass

    def run(self, hostname, ip, port, os, sche_hours, freq_hours):
        self.set_timezone('Europe/Copenhagen')
        self.create_agent(hostname, ip, port, os)
        self.create_disksafe(hostname)
        self.create_policy(hostname, sche_hours, freq_hours)

    def set_timezone(self, area):
        os.environ['TZ'] = area
        time.tzset()

    def create_agent(self, hostname, ip, port, os):
        agent_object = {}
        agent_object['description'] = hostname
        agent_object['hostname'] = ip
        agent_object['portNumber'] = port
        agent_object['osType'] = os
        agent_object['databaseAddOnEnabled'] = False

        agent_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/Agent?wsdl',
                              username=self.soap_user, password=self.soap_pass)

        self.created_agent = agent_client.service.createAgentWithObject(agent_object)

        print('Agent created with id ' + self.created_agent.id + '.')


    def create_disksafe(self, hostname):
        disksafe_object = {}
        disksafe_object['description'] = 'DS.1 ' + hostname
        disksafe_object['agentID'] = self.created_agent.id
        disksafe_object['path'] = '/storage01'
        disksafe_object['compressionType'] = 'QUICKLZ'
        disksafe_object['deviceBackupType'] = 'AUTO_ADD_DEVICES'
        disksafe_object['backupPartitionTable'] = True
        disksafe_object['backupUnmountedDevices'] = True

        disksafe_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/DiskSafe?wsdl',
                              username=self.soap_user, password=self.soap_pass)

        self.created_disksafe = disksafe_client.service.createDiskSafeWithObject(disksafe_object)

        print('Disksafe created with id ' + self.created_disksafe.id + '.')

    def create_policy(self, hostname, replsche_hours_of_day, dailyfreq_hours_of_day):
        policy_object = {}
        repl_sche_freq_vals = {}
        archive_schedule_instance = {}
        daily_frequency_values = {}

        policy_object['enabled'] = True
        policy_object['name'] = hostname + ' daily i2'
        policy_object['description'] = 'daily k15 i2'
        policy_object['diskSafeID'] = self.created_disksafe.id

        policy_object['replicationScheduleFrequencyType'] = 'DAILY'
        repl_sche_freq_vals['startingMinute'] = 0
        repl_sche_freq_vals['hoursOfDay'] = replsche_hours_of_day
        policy_object['replicationScheduleFrequencyValues'] = repl_sche_freq_vals

        policy_object['mergeScheduleFrequencyType'] = 'ON_DEMAND'
        policy_object['diskSafeVerificationScheduleFrequencyType'] = 'ON_DEMAND'
        policy_object['recoveryPointLimit'] = 3
        policy_object['forceFullBlockScan'] = False
        policy_object['multiVolumeSnapshot'] = False

        archive_schedule_instance['archiveScheduleType'] = 'DAILY'
        archive_schedule_instance['retentionCount'] = 15
        daily_frequency_values['startingMinute'] = 0
        daily_frequency_values['hoursOfDay'] = dailyfreq_hours_of_day
        archive_schedule_instance['archiveScheduleFrequencyValues'] = daily_frequency_values

        policy_object['archiveScheduleInstanceList'] = archive_schedule_instance

        policy_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/Policy2?wsdl',
                              username=self.soap_user, password=self.soap_pass)

        self.created_policy = policy_client.service.createPolicy(policy_object)

        print('Policy created with id ' + self.created_policy.id + '.')

    def help(self):
        print('Usage:')
        print('./cdp.py [hostname] [ip] [os (LINUX/WINDOWS)] [scheduled hour] [frequency hours]')

if __name__ == '__main__':

    cdp = cdp('cdp.hostname.tld', '9443', 'admin', 'password')

    if len(sys.argv) > 5:
        cdp.run(sys.argv[1], sys.argv[2], 1167, sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        cdp.help()
