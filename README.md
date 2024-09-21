# PiCar

## To Do

* add motors and keyboard control
* explore tracking solutions

## Software

* GPIO zero: https://gpiozero.readthedocs.io/en/latest/recipes.html#robot
* SenseHat API: https://pythonhosted.org/sense-hat/api/
* Hailo RPi5 Basic Pipelines: https://github.com/hailo-ai/hailo-rpi5-examples/blob/main/doc/basic-pipelines.md#hailo-rpi5-basic-pipelines
* Car Detection and Tracking System for Toll Plazas - Raspberry Pi AI
  Kit: https://docs.edgeimpulse.com/experts/image-projects/vehicle-detection-raspberry-pi-ai-kit
* GStreamer Tutorials: https://gstreamer.freedesktop.org/documentation/tutorials/index.html?gi-language=c
* Multiprocessing in Python: https://www.geeksforgeeks.org/multiprocessing-python-set-1/

## Hardware

### Sense Hat

* About: https://www.raspberrypi.com/documentation/accessories/sense-hat.html
* Pins: https://pinout.xyz/pinout/sense_hat

### AI Kit

* About: https://www.raspberrypi.com/documentation/accessories/ai-kit.html#about

### Camera

* Foxeer Micro Cat 3 1200TVL 0.00001lux Super Low Light Night
  Camera: https://a.co/d/4kiIgj4

## Links

* Night Vision Basics: https://www.youtube.com/watch?v=UAeJHAFjwPM
* Training YOLOv8 model: https://www.youtube.com/watch?v=m9fH9OWn8YM
* YOLOv8 on MAC M1: https://www.youtube.com/watch?v=kEcWUZ8unmc
* YOLOv8 on Raspberry Pi5: https://www.youtube.com/watch?v=ZebczOt90mU

## Installation

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
> source setup_env.sh
> python main.py [options]

Examples:
> python main.py -h                                      (display help)
> python main.py --input rpi --network yolov8s           (use pi camera and 8s yolo model)
> python main.py --input rpi --nv                        (do not output video)
> python main.py -v                                      (print more information)
```

## Tools

```
rpicam-still --list-cameras          (to display attached cameras)
```
