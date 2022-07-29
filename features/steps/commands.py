from behave import *
import cv2
import os
import sys
import json

fpath = os.path.join(os.path.dirname(__file__), 'image_compare')
sys.path.append(fpath)

from image_compare.compare_images import findMatch

@given('Modelo de tv {tvModel}')
def step_impl(context, tvModel):
    print("MODELO DE TV: " + tvModel)
    context.n_captures = 0

@given('Teste prefixo "{testPrefix}"')
def step_impl(context, testPrefix):
    print("PREFIXO: " + testPrefix)
    context.testPrefix = testPrefix

@when('Sequência de comandos "{cmdSequence}"')
def sequence_cmd(context, cmdSequence):
    for cmd in cmdSequence.split(','):
        print('Rodando comando: ' + cmd)
    input("Execute o comando:\n")

@when('Digita "{title}"')
def step_impl(context, title):
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
            sequence_cmd(context, ','.join(moveforward))
        sequence_cmd(context, "enter")
        if len(movebackward):
            sequence_cmd(context, ','.join(movebackward))
        movebackward.clear()
        moveforward.clear()

@when('Executa comando "{cmd}"')
def step_impl(context, cmd):
    print('Rodando comando: ' + cmd)
    #input("Execute o comando:\n")

@when('Captura imagem')
def step_impl(context):
    context.n_captures += 1
    print('Imagem capturada!')
    # initialize the camera
    cam = cv2.VideoCapture(1)   # 0 -> index of camera
    cv2.waitKey(1000)
    s, img = cam.read()
    assert s    # frame captured without any errors
    #cv2.namedWindow("cam-test",cv2.CV_WINDOW_AUTOSIZE)
    #cv2.imshow("cam-test",img)
    #cv2.waitKey(0)
    #cv2.destroyWindow("cam-test")

    filename = "./imgs/" + (context.testPrefix if hasattr(context, 'testPrefix') else "") + str(context.n_captures) + ".jpg"
    if os.environ['TEST_MODE'] == "prepare":
        cv2.imwrite(filename,img) #save image
    
    if os.environ['TEST_MODE'] == "validate":
        imgBase = cv2.imread(filename)
        error = findMatch(img, imgBase)
        print("salvar diferença entre imagens")
        addUpdateField(filename, error)
    
    if os.environ['TEST_MODE'] == "run":
        imgBase = cv2.imread(filename)
        error = findMatch(img, imgBase)
        print("assert diferença entre imagens " + str(error))
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
