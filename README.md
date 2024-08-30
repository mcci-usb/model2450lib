# model2450lib

This is a Python library to control MCCI Model2450 Brightness And Color Kit.

## Install Python3.7 (64-bit) package

install python package from [python.org](https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64.exe)

## Install pip package

```shell
pip --version
python -m pip install --upgrade pip
```

## Prerequisites for running or building

<strong>On Windows:</strong>

Development environment

* OS - Windows 10 and 11 64 bit
* Python - 3.7.8
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
python setup.py install
```

Please navigate to dist/ directory and you will find the files .egg file.
Example: `model2450lib-1.0.0-py3.7.egg`

## How to use the package

Create a Python file and import the class library from package:

```python
from model2450lib import searchmodel
from model2450lib import model2450
```

### Listed out the Model2450

dev_list = searchmodel.get_models()

### Open comport

sw1 = model2450.Model2450('COM3')

### Connect the USB Model

sw1.connect()

### cmd for Read color

sw1.get_color()

### cmd for Read level

sw1.get_level()

### cmd Read

sw1.get_read()

### cmd for sn (serial number)

sw1.read_sn()

### cmd for get Version

sw1.get_version()

## Release History

- v1.0.0 initial release
