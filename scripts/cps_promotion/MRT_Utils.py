import glob
import os
import shutil
import subprocess
from sys import platform
import time
import calendar
import zipfile
import sys
import wget
import ssl
import socket
import requests
import json
import getpass
from configparser import ConfigParser
import datetime
from enum import Enum
import textwrap
import xml.etree.ElementTree as ET
import traceback

FIELDINFO = {}
# ######### Functions #####################
count = 0
wrapperFile = ''
cfg = None
content = None
argumentConfigFile = None

###Share location
share_hostname = 'md1npdvlnx383'
share_port = 22
share_username = 'npd-dcsv'
share_password = 'xxxxxx'
share_Localtion = '/data/npd-dcsv/share/'
share_url = 'http://' + share_hostname + '/share/'

enableDebug = False



def warn(message):
    # print('WARN: ' + message)
    logMessage = 'echo "' + 'WARN: ' + message + '"'
    # print(logMessage)
    # print('INFO: ' + logMessage)
    if isWindows():
        print('WARN: ' + message)
    else:
        print('WARN: ' + message)
def isWindows():
    return platform.lower().startswith('win')

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props
def curlPost(url, data=None, headers=None, key=None):
    debug('API request URL:' + url)
    response = requests.post(url=url, data=data, headers=headers, verify=False)
    if response.text == 'Unauthorized':
        error('Unauthorized')
    debug('API Response:' + str(response.status_code) + '\n     ' + response.text)
    jsonContent = json.loads(response.text)
    if response.status_code >= 400:
        warn('POST API unsuccessful with error:' + response.text)
    if response.status_code >= 200 and response.status_code < 400:
        debug('POST API successful. URL:' + url)

    if key is not None:
        value = jsonContent[key]
        debug('Get key value from json:' + key + ':' + value)
        return value
    else:
        return response

def getOs():
    if isWindows():
        return 'Windows'
    else:
        return 'Linux'

def isURLReachable(url):
    try:
        response = requests.get(url, verify=False)
        http_status_code = response.status_code
        if http_status_code >= 200 and http_status_code < 500:
            return True
        else:
            return False
    except:
        return False

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
def getCurrentDirectoryFiles(dir):
    return glob.glob(dir + os.sep + '*')

def getListFiles(dir, finalList, finalListD):
    for file in getCurrentDirectoryFiles(dir):
        if not os.path.isdir(file):
            finalList.append(file)
        else:
            finalListD.append(file)
            getListFiles(file, finalList, finalListD)


def getFilesList(directory):
    finalList = []
    finalListD = []
    getListFiles(directory, finalList, finalListD)
    return finalList
def curlPut(url, data=None, headers=None, key=None):
    debug('API request URL:' + url)
    response = requests.put(url=url, data=data, headers=headers, verify=False)
    if response.text == 'Unauthorized':
        error('Unauthorized')
    debug('API Response:' + str(response.status_code) + '\n     ' + response.text)
    jsonContent = json.loads(response.text)
    if response.status_code >= 400:
        warn('POST API unsuccessful with error:' + response.text)
    if response.status_code >= 200 and response.status_code < 400:
        debug('POST API successful. URL:' + url)

    if key is not None:
        value = jsonContent[key]
        debug('Get key value from json:' + key + ':' + value)
        return value
    else:
        return response


def enableDebugMessages(status):
    global enableDebug
    enableDebug = status


def debug(message):
    global enableDebug
    if enableDebug:
        print('DEBUG: ' + message)


def error(message):
    print('ERROR: ' + str(message))
    exit(1)
def delete(path):
    try:
        if os.path.exists(path):
            if os.path.isdir(path):
                removeDirectory(path)
            if os.path.isfile(path):
                removeFile(path)
    except:
        debug('Delete error of %s' % (path))

def getEnvValue(key, isMandatory=True):
    global argumentConfigFile
    debug('Getting value for "' + key + '"')
    value = getEnvironmentValue(key)
    if (value is None or value == '') and isMandatory:
        error('"' + key + '" value should not be None or empty.')
    if value is not None:
        if argumentConfigFile is not None:
            debug('[' + key + '="' + value + '"] from configuration file ' + argumentConfigFile)
        else:
            debug('[' + key + '="' + value + '"]')
    else:
        warn(key + ' value is None or empty.')
    return value
def removeDirectory(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def removeFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
def getEnvironmentValue(key):
    loadConfigFile()
    global argumentConfigFile
    if argumentConfigFile is None:
        value = os.environ.get(key)
    else:
        value = getValuesFromConfigFile(key)
    return value

def loadConfigFile():
    global argumentConfigFile
    if argumentConfigFile is None:
        argumentList = sys.argv
        if len(argumentList) > 1:
            if len(argumentList) > 2:
                file = ''
                for countNum in range(len(argumentList)):
                    if countNum > 0:
                        if file == '':
                            file = file + argumentList[countNum]
                        else:
                            file = file + ' ' + argumentList[countNum]
            else:
                file = argumentList[1]
            if not os.path.isfile(file):
                error("File not found:" + file)
            setConfigFile(file)
            argumentConfigFile = file
def getValuesFromConfigFile(key):
    try:
        value = cfg.get(content, key)
    except:
        value = None
    return value

def setConfigFile(configFileName):
    global cfg
    global content
    global configFile
    configFile = configFileName
    cfg = ConfigParser()
    if not os.path.exists(configFileName):
        error(configFileName + ' not existed....!!!.')
    try:
        cfg.read(configFile)
    except:
        error(
            'Invalid configuration file:' + 'Config file "' + configFileName + '" should contains atleast single content section.')
    sectionsCfg = cfg.sections()
    if len(sectionsCfg) == 1:
        content = sectionsCfg.pop()
    else:
        listValue = '['
        for i in sectionsCfg:
            if listValue != '[':
                listValue = listValue + ' , ' + i
            else:
                listValue = listValue + i
        listValue = listValue + ']'
        error(
            'Invalid configuration file:' + 'Config file "' + configFileName + '" should contains only one content section.' + listValue)

