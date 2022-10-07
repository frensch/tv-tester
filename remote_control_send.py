import broadlink
import json
import time
import os
import sys
#devices = broadlink.discover()

#print('devices ' + str(devices))
#device = broadlink.hello("10.0.0.140")
device = broadlink.hello(os.environ['TV_TESTER_IR_REMOTE'])
device.auth()


def getFieldRemoteControl(field):
    try:
        # Read file first
        with open('remote_data.json') as json_file:
            data = json.load(json_file)
            return data[field]
    except IOError:
        return ""

def to_bytes(s):
    #s = s.encode(s,'unicode')
    return bytes(s, encoding='ISO-8859-1')

def send_cmd(cmd):
    print('enviando ' + cmd)
    device.send_data(to_bytes(model[cmd]))

#if len(sys.argv) != 3:
#    print("formato do parametros deve ser [MODELO] [COMANDO]")
#    exit

model = getFieldRemoteControl(sys.argv[1])

