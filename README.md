## Install
Using python 3
```
virtualenv venv     
source venv/bin/activate
pip install -r requirements.txt
```
## Config

### Camera
You need to configure the camera and the IR Remote device.
The Camera should work any IP or USB model, but I have tested with a IP camera from ONVIF and a USB camera
You have to fill the environment variable ```TV_TESTER_CAMERA```
#### USB example
export TV_TESTER_CAMERA=0

### IP example
export TV_TESTER_CAMERA=rtsp://admin:brewedattheeagle1@192.168.0.44:554/onvif1

### IR Remote Device
The IR Remote device must be a Broadlink device, because of the library I used.
You have to fill the environment variable ```TV_TESTER_IR_REMOTE```

#### IR Remote example
export TV_TESTER_IR_REMOTE=192.168.0.173


## Usage
### capture
This mode will start learning how the app should behave. It should be excuted in a stable version.
The commands will be sent to the the tv and the camera will captured and save the images only.
Run the script ```capture.sh```

### validate
This mode will calculate the range of the capture error. It should be excuted in a stable version.
The commands will be sent to the the tv and the camera will captured the same images and compared the differences and estimate the capturing error of the same images.
Run the script ```validate.sh```


### run
This mode will be used to run the tests in the version you want to be tested.
The commands will be sent to the the tv and the camera will captured and compared with the previous captured images for the assertion of the tests.
Run the script ```run.sh```
