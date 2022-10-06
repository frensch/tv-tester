from behave import *
import cv2
import os
import sys
import json
import broadlink
import time

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

fpath = os.path.join(os.path.dirname(__file__), 'image_compare')
sys.path.append(fpath)

from image_compare.compare_images import findMatch

if os.environ["TV_TESTER_CAMERA"].isnumeric():
    cam = cv2.VideoCapture(int(os.environ["TV_TESTER_CAMERA"]))
else:
    cam = cv2.VideoCapture(os.environ["TV_TESTER_CAMERA"], cv2.CAP_FFMPEG)
time.sleep(5) # wait for the camera to normalize the image

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


@when('load the tv model {tvModel}')
def step_impl(context, tvModel):
    print("TV MODEL: " + tvModel)
    context.n_captures = 0
    context.tv = getFieldRemoteControl(tvModel)


@given('test prefix "{testPrefix}"')
def step_impl(context, testPrefix):
    print("PREFIXO: " + testPrefix)
    context.testPrefix = testPrefix

@when('run command "{cmd}" for {times:d} times and wait {secs:g} second(s)')
def cmd_times(context, cmd, times, secs):
    for t in range(0, times):
        print('Rodando comando: ' + cmd)
        exec_cmd(context, cmd, 0.6)
    time.sleep(secs)
    #input("Execute o comando:\n")

@when('sequence of commands "{cmdSequence}" and wait {secs:g} second(s)')
def sequence_cmd(context, cmdSequence, secs):
    for cmd in cmdSequence.split(','):
        print('Rodando comando: ' + cmd)
        exec_cmd(context, cmd, 0.6)
    time.sleep(secs)
    #input("Execute o comando:\n")

@when('typing "{title}" and wait {secs:g} second(s)')
def step_impl(context, title, secs):
    moveforward = []
    movebackward = []
    for c in title:
        numLetter = ord(c) - 97
        print('letter: ' + c + str(numLetter))
        for i in range(0, numLetter % 6):
            moveforward.append("right")
            movebackward.append("left")
        for i in range(0,int(numLetter / 6)):
            moveforward.append("down")
            movebackward.append("up")

        if len(moveforward):
            sequence_cmd(context, ','.join(moveforward), 0.6)
        sequence_cmd(context, "enter", 0.6)
        if len(movebackward):
            sequence_cmd(context, ','.join(movebackward), 0.6)
        movebackward.clear()
        moveforward.clear()
    time.sleep(secs)

@when('waiting {secs:g} second(s)')
def step_impl(context, secs):
    time.sleep(secs)

@when('run command "{cmd}" and wait {secs:g} second(s)')
def exec_cmd(context, cmd, secs):
    print('Rodando comando: ' + cmd)
    device.send_data(to_bytes(context.tv[cmd]))
    time.sleep(secs)
    #input("Execute o comando:\n")

@when('capture image')
def step_impl(context):
    context.n_captures += 1
    print('Imagem capturada!')
    # initialize the camera
    #cam = cv2.VideoCapture(1)   # 0 -> index of camera
    cv2.waitKey(1000)
    s, img = cam.read()
    assert s    # frame captured without any errors
    #cv2.namedWindow("cam-test",cv2.CV_WINDOW_AUTOSIZE)
    #cv2.imshow("cam-test",img)
    #cv2.waitKey(0)
    #cv2.destroyWindow("cam-test")

    filename = "./imgs/" + (context.testPrefix if hasattr(context, 'testPrefix') else "") + str(context.n_captures) + ".jpg"
    if os.environ['TEST_MODE'] == "capture":
        cv2.imwrite(filename,img) #save image
    
    if os.environ['TEST_MODE'] == "validate":
        imgBase = cv2.imread(filename)
        error = findMatch(img, imgBase)
        print("salvar diferença entre imagens")
        addUpdateField(filename, error)
    
    if os.environ['TEST_MODE'] == "run":
        imgBase = cv2.imread(filename)
        error = findMatch(img, imgBase)
        print("assert diferença entre imagens " + filename + ' | ' + str(error))
        expected_error = 3*getField(filename)
        if(error > expected_error):
            cv2.imwrite(filename + '_error.jpg',img) #save image
            
        assert error < 3*getField(filename)

def getField(field):
    try:
        # Read file first
        with open('test_data.json') as json_file:
            data = json.load(json_file)
            print(data)
            return data[field]
    except IOError:
        return ""

def addUpdateField(field, value):
    data = {}
    try:
        # Read file first
        with open('test_data.json') as json_file:
            data = json.load(json_file)
            print(data)
    except IOError as e:
        pass        
    data[field] = value
    # Write directly from dictionary
    with open('test_data.json', 'w') as outfile:
        json.dump(data, outfile)
