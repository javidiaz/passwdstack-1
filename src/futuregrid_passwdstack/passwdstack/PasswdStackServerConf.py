#!/usr/bin/env python
# -------------------------------------------------------------------------- #
# Copyright 2010-2011, Indiana University                                    #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #
"""
Class to read Passwd Stack Server configuration
"""

import os
import ConfigParser
import string
import sys
import logging
import re

configFileName = "fg-server.conf"

class PasswdStackServerConf(object):

    ############################################################
    # init
    ############################################################

    def __init__(self):
        super(PasswdStackServerConf, self).__init__()

        self._fgpath = ""
        try:
            self._fgpath = os.environ['FG_PATH']
        except KeyError:
            self._fgpath = os.path.dirname(__file__) + "/../../"

        ##DEFAULT VALUES##
        self._localpath = "~/.fg/"

        self._configfile = os.path.expanduser(self._localpath) + "/" + configFileName
        #print self._configfile
        if not os.path.isfile(self._configfile):
            self._configfile = "/etc/futuregrid/" + configFileName #os.path.expanduser(self._fgpath) + "/etc/" + configFileName
            #print self._configfile
            #if not os.path.isfile(self._configfile):
            #    self._configfile = os.path.expanduser(os.path.dirname(__file__)) + "/" + configFileName
                #print self._configfile
            if not os.path.isfile(self._configfile):   
                print "ERROR: configuration file "+configFileName+" not found"
                sys.exit(1)
        
        #image generation server
        self._port = 0
        self._proc_max = 0
        self._refresh_status = 0
        self._log = ""
        self._logLevel=""
        self._ca_certs = ""
        self._certfile = ""
        self._keyfile = ""

        
        self._logLevel_default = "DEBUG"
        self._logType = ["DEBUG", "INFO", "WARNING", "ERROR"]
        
        self._config = ConfigParser.ConfigParser()
        self._config.read(self._configfile)

    ############################################################
    # getConfigFile
    ############################################################
    def getConfigFile(self):
        return self._configfile
    
    #image generation server
    def getPort(self):
        return self._port
    def getProcMax(self):
        return self._proc_max
    def getRefreshStatus(self):
        return self._refresh_status

    def getLog(self):
        return self._log
    def getLogLevel(self):
        return self._logLevel
    def getCaCerts(self):
        return self._ca_certs
    def getCertFile(self): 
        return self._certfile
    def getKeyFile(self): 
        return self._keyfile
    
    ############################################################
    # load_generateServerConfig
    ############################################################
    def load_passwdstackServerConfig(self):        
        section = "PasswdStackServer"
        try:
            self._port = int(self._config.get(section, 'port', 0))
        except ConfigParser.NoOptionError:
            print "Error: No port option found in section " + section + " file " + self._configfile
            sys.exit(1)
        except ConfigParser.NoSectionError:
            print "Error: no section "+section+" found in the "+self._configfile+" config file"
            sys.exit(1)
        try:
            self._proc_max = int(self._config.get(section, 'proc_max', 0))
        except ConfigParser.NoOptionError:
            print "Error: No proc_max option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            self._refresh_status = int(self._config.get(section, 'refresh', 0))
        except ConfigParser.NoOptionError:
            print "Error: No refresh option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            aux = self._config.get(section, 'nopasswdusers', 0).strip()
            aux = "".join(aux.split()) #REMOVE ALL WHITESPACES
            parts = aux.split(";")
            for i in parts:         
                temp = i.split(":")
                if len(temp) == 2:                    
                    self._nopasswdusersgen[temp[0]] = temp[1].split(",")            
        except ConfigParser.NoOptionError:            
            pass
       
        try:
            self._log = os.path.expanduser(self._config.get(section, 'log', 0))
        except ConfigParser.NoOptionError:
            print "Error: No log option found in section " + section + " file " + self._configfile
            sys.exit(1)
        try:
            tempLevel = string.upper(self._config.get(section, 'log_level', 0))
        except ConfigParser.NoOptionError:
            tempLevel = self._logLevel_default
        if not (tempLevel in self._logType):
            print "Log level " + tempLevel + " not supported. Using the default one " + self._logLevel_default
            tempLevel = self._logLevel_default
        self._logLevel = eval("logging." + tempLevel)
        
        try:
            self._ca_certs = os.path.expanduser(self._config.get(section, 'ca_cert', 0))
        except ConfigParser.NoOptionError:
            print "Error: No ca_cert option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._ca_certs):
            print "Error: ca_cert file not found in "  + self._ca_certs 
            sys.exit(1)
        try:
            self._certfile = os.path.expanduser(self._config.get(section, 'certfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No certfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._certfile):
            print "Error: certfile file not found in "  + self._certfile 
            sys.exit(1)
        try:
            self._keyfile = os.path.expanduser(self._config.get(section, 'keyfile', 0))
        except ConfigParser.NoOptionError:
            print "Error: No keyfile option found in section " + section + " file " + self._configfile
            sys.exit(1)
        if not os.path.isfile(self._keyfile):
            print "Error: keyfile file not found in "  + self._keyfile 
            sys.exit(1)
        