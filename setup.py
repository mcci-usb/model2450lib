##############################################################################
# 
# Module: setup.py
#
# Description:
#     setup to install the model2450lib package
#
#         MCCI Corporation
#         3520 Krums Corners Road
#         Ithaca, NY  14850
#
# Author:
#     Vinay N, MCCI Corporation Feb 16 2026
#
# Revision history:
#     v2.1.0  Wed Feb 16 2026 12:05:00  Vinay N
#         Module created
#
##############################################################################

from setuptools import setup, find_packages

setup(
    name="model2450lib",  # A single string, the package's name
    version="2.1.0",
    packages=find_packages(),  # Automatically includes subpackages like 'model2450lib.serial'
    include_package_data=True,
    install_requires=["pyserial>=3.5"],
)

