# Turntable Control GUI

**Version 0.1v**

## Overview

Turntable Control GUI is a simple Python application built with Tkinter and PySerial that allows you to control a turntable via a COM port. The application supports both preset movements (1°, 5°, 10°, 45°, 90°) and custom angles. It converts degrees into steps (using the conversion factor of **1° = 31.205 steps**), sends commands to the turntable, and tracks the current angle. A reset feature is provided to return the turntable to its starting position (0°).

## Features

- **COM Port Connection:** Easily connect to a specified COM port with a configurable baud rate.
- **Preset Angle Movements:** Move the turntable by +1°, +5°, +10°, +45°, +90° and their negative counterparts.
- **Custom Angle Input:** Enter a custom angle value for more precise control.
- **Degree to Step Conversion:** Automatically converts degrees to steps (1° = 31.205 steps).
- **Position Tracking:** The GUI displays the current turntable angle.
- **Reset Functionality:** Quickly return the turntable to its original position (0°).
- **Logging:** Displays sent and received commands for troubleshooting.

## Requirements

- Python 3.x
- Tkinter (usually bundled with Python)
- PySerial
  
**Install via pip:**
```bash
  pip install pyserial
```
## (Optional) PyInstaller for creating standalone executables
(Optional) PyInstaller for creating standalone executables
Install via pip:
  ```bash
  pip install pyinstaller
  ```
##Installation
  
### Clone the Repository:
   ```bash
   git clone https://github.com/foxybbb/hp_3d_turnable.git
   ```
### Navigate to the Project Directory:
```bash
cd hp_3d_turnable
```
### (Optional) Create and Activate a Virtual Environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
### Install Required Packages: If a requirements.txt file is provided:
```bash
pip install -r requirements.txt
```
### Otherwise, manually install PySerial:
```bash
    pip install pyserial
```
### Usage

### Run the Application:
```bash
python main.py
```
