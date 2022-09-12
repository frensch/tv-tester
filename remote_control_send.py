import broadlink
import json
import time
#devices = broadlink.discover()

#print('devices ' + str(devices))
#device = broadlink.hello("10.0.0.140")
device = broadlink.hello("192.168.0.173")
device.auth()


def getFieldRemoteControl(field):
    try:
        # Read file first
        with open('remote_data.json') as json_file:
            data = json.load(json_file)
            print(data)
            return data[field]
    except IOError:
        return ""

def to_bytes(s):
    #s = s.encode(s,'unicode')
    return bytes(s, encoding='ISO-8859-1')

model = getFieldRemoteControl('samsung')

print('enviando ligar ' + str(to_bytes(model['power'])))
device.send_data(to_bytes(model['down']))
time.sleep(1)

device.send_data(to_bytes(model['down']))
time.sleep(1)


device.send_data(to_bytes(model['up']))
time.sleep(1)


device.send_data(to_bytes(model['up']))
time.sleep(1)

device.send_data(to_bytes(model['enter']))
time.sleep(1)
#key = input("Esperando comando:\n")


#print('enviando enter')
#device.send_data(packets[1])
