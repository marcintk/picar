# PiCar

Project to experiment with Raspberry Pi 5, AI Kit, Sense Kit and Robot.

## Hardware

### AI Kit

* About: https://www.raspberrypi.com/documentation/accessories/ai-kit.html#about

### Sense Hat

* About: https://www.raspberrypi.com/documentation/accessories/sense-hat.html
* Pins: https://pinout.xyz/pinout/sense_hat

## Software

* Robot API: https://gpiozero.readthedocs.io/en/latest/recipes.html#robot
* SenseHat API: https://pythonhosted.org/sense-hat/api/

## Links

* Car Detection and Tracking System for Toll Plazas - Raspberry Pi AI Kit:
  https://docs.edgeimpulse.com/experts/image-projects/vehicle-detection-raspberry-pi-ai-kit
* Object Detection with Tracking using ByteTracker and Supervision:
  https://github.com/hailo-ai/Hailo-Application-Code-Examples/blob/main/runtime/python/detection_with_tracker/README.md
* Hailo RPi5 Basic Pipelines:
  https://github.com/hailo-ai/hailo-rpi5-examples/blob/main/doc/basic-pipelines.md#hailo-rpi5-basic-pipelines
* GStreamer Tutorials:
  https://gstreamer.freedesktop.org/documentation/tutorials/index.html?gi-language=c
* Multiprocessing in Python:
  https://www.geeksforgeeks.org/multiprocessing-python-set-1/

## Installation

```
# https://www.raspberrypi.com/documentation/accessories/ai-kit.html#install
> sudo apt update && sudo apt full-upgrade
> sudo apt install hailo-all

# https://www.raspberrypi.com/documentation/accessories/sense-hat.html#install
> sudo apt install sense-hat

> sudo reboot

> source setup_env.sh
> pip install --upgrade pip
> pip install -r requirements.txt
```

### Issues:

#### LGPIO :https://forums.raspberrypi.com/viewtopic.php?t=362657

```
> sudo apt remove python3-rpi.gpio
> pip3 install rpi-lgpio
```

## Usage

```
> source setup_env.sh
> python main.py [options]
or
> run.sh [options]

Examples:
> python main.py -h                                      (display help)
> python main.py --input rpi --network yolov8s           (use pi camera and 8s yolo model)
> python main.py --input rpi --nv                        (do not output video)
> python main.py -v                                      (print more information)
```

## Tools

```
rpicam-still --list-cameras          (to display attached cameras)
hailortcli fw-control identify       (status of hailo)
```

## To Do

* add motors and keyboard control
* explore tracking solutions
