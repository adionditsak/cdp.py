#!/usr/bin/env python

import os
import sys
import time
import suds
from suds.client import Client


class CreateIderaBackup():

  def __init__(self, soap_host, soap_port, soap_user, soap_pass):

    self.soap_host = soap_host
    self.soap_port = soap_port
    self.soap_user = soap_user
    self.soap_pass = soap_pass

  def run(self, hostname, ip, port, os):

    self.set_timezone('Europe/Copenhagen')
    self.create_agent(hostname, ip, port, os)
    self.create_disksafe(hostname)
    self.create_policy(hostname)

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

    try:
      agent_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/Agent?wsdl', username=self.soap_user, password=self.soap_pass)
      self.created_agent = agent_client.service.createAgentWithObject(agent_object)
      print('Agent created with id ' + self.created_agent.id + '.')
    except suds.WebFault as e:
      print('Failed to create agent:')
      print(e)

  def create_disksafe(self, hostname):

    disksafe_object = {}
    disksafe_object['description'] = 'DS.1 ' + hostname
    disksafe_object['agentID'] = self.created_agent.id
    disksafe_object['path'] = '/storage01'
    disksafe_object['compressionType'] = 'QUICKLZ'
    disksafe_object['deviceBackupType'] = 'AUTO_ADD_DEVICES'
    disksafe_object['backupPartitionTable'] = True
    disksafe_object['backupUnmountedDevices'] = True

    try:
      disksafe_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/DiskSafe?wsdl', username=self.soap_user, password=self.soap_pass)
      self.created_disksafe = disksafe_client.service.createDiskSafeWithObject(disksafe_object)
      print('Disksafe created with id ' + self.created_disksafe.id + '.')
    except suds.WebFault as e:
      print('Failed to create disksafe:')
      print(e)

  def create_policy(self, hostname):

    policy_object = {}
    repl_sche_freq_vals = {}
    archive_schedule_instance = {}
    daily_frequency_values = {}

    policy_object['enabled'] = True
    policy_object['name'] = hostname + ' daily'
    policy_object['description'] = 'daily k15'
    policy_object['diskSafeID'] = self.created_disksafe.id

    policy_object['replicationScheduleFrequencyType'] = 'DAILY'
    repl_sche_freq_vals['startingMinute'] = 0
    repl_sche_freq_vals['hoursOfDay'] = 2
    policy_object['replicationScheduleFrequencyValues'] = repl_sche_freq_vals

    policy_object['mergeScheduleFrequencyType'] = 'ON_DEMAND'
    policy_object['recoveryPointLimit'] = 3
    policy_object['forceFullBlockScan'] = False
    policy_object['multiVolumeSnapshot'] = False

    archive_schedule_instance['archiveScheduleType'] = 'DAILY'
    archive_schedule_instance['retentionCount'] = 15
    daily_frequency_values['startingMinute'] = 0
    daily_frequency_values['hoursOfDay'] = 17
    archive_schedule_instance['archiveScheduleFrequencyValues'] = daily_frequency_values

    policy_object['archiveScheduleInstanceList'] = archive_schedule_instance

    try:
      policy_client = Client('https://' + self.soap_host + ':' + self.soap_port + '/Policy2?wsdl', username=self.soap_user, password=self.soap_pass)
      self.created_policy = policy_client.service.createPolicy(policy_object)
      print('Policy created with id ' + self.created_policy.id + '.')
    except suds.WebFault as e:
      print('Failed to create policy:')
      print(e)

  def help(self):
    print('Usage:')
    print('./CreateIderaBackup.py [hostname] [ip] [os (LINUX/WINDOWS)]')

if __name__ == '__main__':

  cib = CreateIderaBackup('ideraserver01.tld', '9443', 'IderaAdmin', 'IderaPassword')

  if len(sys.argv) > 3:
    cib.run(sys.argv[1], sys.argv[2], 1167, sys.argv[3])
  else:
    cib.help()
