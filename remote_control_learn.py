import broadlink
import json
#devices = broadlink.discover()

#print('devices ' + str(devices))
#device = broadlink.hello("10.0.0.140")
device = broadlink.hello("192.168.0.173")
device.auth()

model = input('digite o modelo de tv ')

def lean_cmd(cmd_name):
    print("iniciar aprendizado")
    device.enter_learning()
    input("Esperando aprendizado: " + cmd_name)
    packet = device.check_data()
    print("packet: " + str(packet))
    return packet.decode('ISO-8859-1')

cmds = {}
cmds['power'] = lean_cmd('power')
cmds['enter'] = lean_cmd('enter')
cmds['up'] = lean_cmd('up')
cmds['left'] = lean_cmd('left')
cmds['down'] = lean_cmd('down')
cmds['right'] = lean_cmd('right')
cmds['home'] = lean_cmd('home')
cmds['back'] = lean_cmd('back')
cmds['globoplay'] = lean_cmd('globoplay')

def addUpdateField(field, value):
    data = {}
    try:
        # Read file first
        with open('remote_data.json') as json_file:
            data = json.load(json_file)
            print(data)
    except IOError as e:
        pass        
    data[field] = value
    # Write directly from dictionary
    with open('remote_data.json', 'w') as outfile:
        json.dump(data, outfile)

addUpdateField(model, cmds)

#print('enviando ligar')
#device.send_data(packets[0])

#key = input("Esperando comando:\n")


#print('enviando enter')
#device.send_data(packets[1])
