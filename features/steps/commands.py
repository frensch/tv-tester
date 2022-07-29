from behave import *
import cv2
import os
import sys
from cv2 import imread

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
def step_impl(context, cmdSequence):
    for cmd in cmdSequence.split(','):
        print('Rodando comando: ' + cmd)
    input("Execute o comando:\n")

@when('Executa comando "{cmd}"')
def step_impl(context, cmd):
    print('Rodando comando: ' + cmd)
    input("Execute o comando:\n")

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
        print("salvar diferença entre imagens")
    
    if os.environ['TEST_MODE'] == "run":
        imgBase = imread(filename)
        error = findMatch(img, imgBase)
        print("assert diferença entre imagens " + str(error))
        assert error < 10000
