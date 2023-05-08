from setuptools import setup
import os
from traffic_monitor import __version__

# Read the contents of the README file
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='traffic_monitor',
    version=__version__,
    packages=['traffic_monitor'],
    install_requires=[
        'dataclasses',
        'pytest',
    ],
    python_requires='>=3.6',

    author='Filipe Rosa',
    description='HTTP traffic monitor from stdin or csv file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'monitor=traffic_monitor.monitor:monitor'
        ]
    }
)