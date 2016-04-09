#!/usr/bin/python
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#import visitors
from visitors.evil_sensor import *
import config
from scapy.all import *
from scapy.fields import ConditionalField
import struct
from datetime import datetime
import pprint
import requests
import json
import config
from os import system
#from visitors import setup_interface


def main():
    global node_name
    if len(sys.argv) < 2:
        print "Please specify evil network interface"
        sys.exit(1)
    if len(sys.argv) >= 3:
        node_name = sys.argv[2]
    evil_interface = sys.argv[1]

    print "[%s] Quely starting sensor" % datetime.now()
    setup_interface(evil_interface)
    set_node_name()
    
    #patch_send() # useful for debugging
    sniff(iface=evil_interface, prn=PacketHandler, store=0)
    
if __name__=="__main__":
    main()


