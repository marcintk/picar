# PiCar

## Tasks

* build project files
* run simple person detection
* add motors and keyboard control
* explore tracking solutions

## Software

* GPIO zero: https://gpiozero.readthedocs.io/en/latest/recipes.html#robot
* SenseHat API: https://pythonhosted.org/sense-hat/api/
* Hailo RPi5 Basic Pipelines: https://github.com/hailo-ai/hailo-rpi5-examples/blob/main/doc/basic-pipelines.md#hailo-rpi5-basic-pipelines
* Car Detection and Tracking System for Toll Plazas - Raspberry Pi AI Kit: https://docs.edgeimpulse.com/experts/image-projects/vehicle-detection-raspberry-pi-ai-kit
* GStreamer Tutorials: https://gstreamer.freedesktop.org/documentation/tutorials/index.html?gi-language=c
* Multiprocessing in Python: https://www.geeksforgeeks.org/multiprocessing-python-set-1/
* 

## Hardware

### Sense Hat

* About: https://www.raspberrypi.com/documentation/accessories/sense-hat.html
* Pins: https://pinout.xyz/pinout/sense_hat

### AI Kit

* About: https://www.raspberrypi.com/documentation/accessories/ai-kit.html#about


### AI board

* RASPBERRY PI 5: https://www.raspberrypi.com/products/raspberry-pi-5/
* ORANGE PI: http://www.orangepi.org/
* JETSON NANO (nvidia): https://developer.nvidia.com/buy-jetson?product=jetson_nano&location=US
* Coral USB accelerator: https://a.co/d/dZcaVqX

### Camera

* Foxeer Micro Cat 3 1200TVL 0.00001lux Super Low Light Night
  Camera: https://a.co/d/4kiIgj4

## Links

* Night Vision Basics: https://www.youtube.com/watch?v=UAeJHAFjwPM
* Training YOLOv8 model: https://www.youtube.com/watch?v=m9fH9OWn8YM
* YOLOv8 on MAC M1: https://www.youtube.com/watch?v=kEcWUZ8unmc
* YOLOv8 on Raspberry Pi5: https://www.youtube.com/watch?v=ZebczOt90mU

## Installation

### OpenCV (optional)

#### Raspberry Pi5

* Info Source: https://qengineering.eu/install%20opencv%20on%20raspberry%20pi%205.html

```
download, compile and build openCV
> cd install/raspberryPi5
> ./opencv_install_custom.sh
```

### Coral TPU

```
> cd install/coral-tpu
Read and execute install_apex.md

> install_python3.9.sh

> cd ../..
> export PATH=$PWD/.python/bin:$PATH
> python3 --version
Python 3.9.9
> python3 -m venv venv
> pip3 install -r requirements.txt
> source venv/bin/activate
```

### Application

```
upgrade system libraries
> sudo apt update
> sudo apt upgrade

install pip3 and python        (if needed)
> pip3 --version               (check the latest installed)
> sudo apt install python3

install python libraries to the virtual environment
> pip3 install -r requirements.txt
```

## Usage

```
> python main.py                                         (press q for exit)

Examples:
> python main.py -h                                      (display help and possible paremeters)
> python main.py -rtsp -fr 640 320                       (use rtps input and resize image)
> python main.py -vi media/car-and-pedestrian-video.mp4  (use video file as an input)
> python main.py -cu=mps                                 (use MPS instead of CPU)
> python main.py --no-display                            (do not show a video display)
> python main.py -d=NONE                                 (drop detection)
> python main.py -v                                      (print more information)
```

## Tools

```
rpicam-still --list-cameras          (to display attached cameras)
```

### Camera

Create '.env' file in the main directory with 4 properties:

```
CAMERA_IP=<IP>:<PORT>
CAMERA_CHANNEL=<CHANNEL>
CAMERA_USER=<USER>
CAMERA_PASSWORD=<PASS>
```
