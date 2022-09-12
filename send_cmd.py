import sys
import broadlink
import time
import json 

device = broadlink.hello("192.168.0.2")
tv = ""

def getFieldRemoteControl(field):
    try:
        # Read file first
        with open('remote_data.json') as json_file:
            data = json.load(json_file)
            return data[field]
    except IOError:
        return ""

def to_bytes(s):
    return bytes(s, encoding='ISO-8859-1')


def load_tv_model(tvModel):
    print("TV MODEL: " + tvModel)
    return getFieldRemoteControl(tvModel)


def sequence_cmd(tv, cmdSequence, secs):
    for cmd in cmdSequence.split(','):
        print('Rodando comando: ' + cmd)
        exec_cmd(tv, cmd, 0.6)
    time.sleep(secs)
    #input("Execute o comando:\n")

def exec_cmd(tv, cmd, secs):
    print('Rodando comando: ' + cmd)
    device.send_data(to_bytes(tv[cmd]))
    time.sleep(secs)
    #input("Execute o comando:\n")

cmd = sys.argv[1]

wait = 2
if len(sys.argv) >= 4:
    wait = sys.argv[3]


tv = load_tv_model(sys.argv[1])
sequence_cmd(tv, sys.argv[2], wait)