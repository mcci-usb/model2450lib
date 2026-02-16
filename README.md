# model2450lib

Python library to control the MCCI Model 2450 Brightness And Color Kit (BACK).

Provides APIs for device discovery, serial communication, sensor data acquisition,color calibration, streaming, and blank frame detection.

## Install Python3.14 (64-bit) package

install python package from [python.org](https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe)

## Install pip package

```shell
pip --version
python -m pip install --upgrade pip
```

## Prerequisites for running or building

<strong>On Windows:</strong>

Development environment

* OS - Windows 10 and 11 64 bit
* Python - 3.14.3
* pyserial - 3.5

<strong>On Linux:</strong>

Development environment

* Ubuntu OS - 24.04
* Python - 3.14.3
* pyserial - 3.5

<strong>On Macos:</strong>

Development environment

* Mac OS Montery - 12.7.6
* Python - 3.14.3
* pyserial - 3.5

```shell
pip install pyserial
```

### Installing Python Packages with Setup.py

1. Clone the repository from [github](https://github.com/mcci-usb/model2450lib)

2. Open a terminal window and change directory to  `{path_to_repository}/model2450lib`. using `cd` into the root directory where setup.py is located

3. To install the library in your local Python

setup, enter the command

```bash
pip install .
```

Please navigate to dist/ directory and you will find the files .egg file.
Example: `model2450lib-2.1.0-py3.7.egg`

## How to use the package

Create a Python file and import the class library from package:

```python
from model2450lib import searchmodel
from model2450lib import model2450
import time
```

### Listed out the Model2450

dev_list = searchmodel.get_models()

### Open comport

```
Replace 'COM3' with the appropriate COM port for Model2450
```
sw1 = model2450.Model2450('COM3')

#### Connect the USB Model

sw1.connect()

#### Read Color Sensor

- Retrieve RGB color values from the BH1749 color sensor.

```
sw1.get_color()
```

#### Read Light Level

- Get the configured blank frame detection threshold.

```
sw1.get_level()
```

#### Read Ambient Light

- Fetch the device serial number stored in EEPROM.

```
sw1.get_read()
```

#### Get Firmware & Hardware Version

- Displays firmware and hardware version (Format F:H)

```

sw1.get_version()
```

#### Set Blank Frame Level

```
# Example (120)
sw1.set_level(120) 
```

#### Calibrate red

- This command calibrates the red color.

```
sw1.set_red()
```

#### Calibrate Green

- This command calibrates the green color.

```
sw1.set_green()
```

#### Calibrate Blue

- This command calibrates the blue color

```
sw1.set_blue()
```

#### Read Serial Number

- Read Serial number.

```
sw1.read_sn()
```

## Release History.

- v2.1.0 Adding Headers
- v2.0.0 Adding Packetazation Format decoding
- v1.0.2 adding decoding packetaizaton
- v1.0.1 update examples
- v1.0.0 initial release
