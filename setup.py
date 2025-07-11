##############################################################################
# 
# Module: setup.py
#
# Description:
#     setup to install the cricklib package
#
#         MCCI Corporation
#         3520 Krums Corners Road
#         Ithaca, NY  14850
#
# Author:
#     Vinay N , MCCI Corp  July, 2024
#
##############################################################################

from setuptools import setup, find_packages

setup(
    name="model2450lib",  # A single string, the package's name
    version="2.0.0",
    packages=find_packages(),  # Automatically includes subpackages like 'model2450lib.serial'
    include_package_data=True,
    install_requires=[],
)

