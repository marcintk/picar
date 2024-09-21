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

## Links

* Night Vision Basics: https://www.youtube.com/watch?v=UAeJHAFjwPM

## Installation

### Application

```
upgrade system libraries
> sudo apt update
> sudo apt upgrade
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
hailortcli fw-control identify       (status of hailo)
```
