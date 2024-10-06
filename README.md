# PiCar

Project experimenting with Raspberry Pi 5, AI Kit, Sense Kit and Robot.

![robot](docs/images/robot.png)

## Hardware

* Raspberry Pi 5: https://www.raspberrypi.com/products/raspberry-pi-5/
* Raspberry AI Kit: https://www.raspberrypi.com/documentation/accessories/ai-kit.html#about
* Raspberry Sense Hat: https://www.raspberrypi.com/documentation/accessories/sense-hat.html
* DC Converter 12v to 5v, 5A: https://www.amazon.com/gp/product/B0D146WV15/
* Wheel Chassis Car Kit: https://www.amazon.com/gp/product/B09CPZ51N4/

## Software

* Robot API: https://gpiozero.readthedocs.io/en/latest/recipes.html#robot
* SenseHat API: https://pythonhosted.org/sense-hat/api/

## Links

* Car Detection and Tracking System for Toll Plazas - Raspberry Pi AI
  Kit: https://docs.edgeimpulse.com/experts/image-projects/vehicle-detection-raspberry-pi-ai-kit
* Object Detection with Tracking using ByteTracker and
  Supervision: https://github.com/hailo-ai/Hailo-Application-Code-Examples/blob/main/runtime/python/detection_with_tracker/README.md
* Hailo RPi5 Basic Pipelines: https://github.com/hailo-ai/hailo-rpi5-examples/blob/main/doc/basic-pipelines.md#hailo-rpi5-basic-pipelines
* Hailo Zoo: https://github.com/hailo-ai/hailo_model_zoo
* GStreamer Tutorials: https://gstreamer.freedesktop.org/documentation/tutorials/index.html?gi-language=c
* Multiprocessing in Python: https://www.geeksforgeeks.org/multiprocessing-python-set-1/
* Sense Hat Pins: https://pinout.xyz/pinout/sense_hat

## Installation

```
# https://www.raspberrypi.com/documentation/accessories/ai-kit.html#install
> sudo apt update && sudo apt full-upgrade
> sudo apt install hailo-all

# https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#pcie-gen-3-0
enable PCIe Gen 3.0, this is optional, not certifed for Raspberry Pi5

# https://www.raspberrypi.com/documentation/accessories/sense-hat.html#install
> sudo apt install sense-hat (should be already present in the system)

> sudo reboot

# verification
> hailortcli fw-control identify
Executing on device: 0000:01:00.0
Identifying board
Control Protocol Version: 2
Firmware Version: 4.18.0 (release,app,extended context switch buffer)
Logger Version: 0
Board Name: Hailo-8
Device Architecture: HAILO8L
Serial Number: HLDDLBB242600712
Part Number: HM21LB1C2LAE
Product Name: HAILO-8L AI ACC M.2 B+M KEY MODULE EXT TMP

> git clone https://github.com/marcintk/picar
> cd picar
> source setup_env.sh
> pip install --upgrade pip
> pip install -r requirements.txt
```

## Usage

```
> source setup_env.sh
> python main.py [options]
or
> run.sh [options]

Examples:
> python main.py -h                                      (display help)
> python main.py --input rpi --network yolov6n           (use pi camera and 6n yolo model)
> python main.py --input rpi -nv                         (do not output video)
> python main.py -v                                      (print more information)
```

## Tools

```
rpicam-still --list-cameras          (to display attached cameras)
hailortcli fw-control identify       (status of hailo)
```

## To Do

* explore tracking solutions
