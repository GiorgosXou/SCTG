from setuptools import setup
import sys


if sys.version_info.major < 3:
    sys.exit('Python < 3 is unsupported (for now).')


setup(
    name="sctg",
    version="0.1.0",
    description="A cross-platform YOLO enhanced, tagging, screenshot app that tags\\stores detected objects within image's EXIF's UserComment entry.",
    author="George Chousos",
    author_email="gxousos@gmail.com",
    url="https://github.com/GiorgosXou/SCTG",
    packages=['sctg'],
    package_data={'sctg': ['icons/*.*', 'nn_files/*.*']},
    install_requires=['opencv-python', 'numpy', 'pyautogui', 'piexif', 'pynput', 'notify-py', 'pillow'],
    entry_points={
        'console_scripts': [
            'sctg = sctg.__init__:main'
            ]
        },
    zip_safe=False
)

# pip3 install .
# python setup.py sdist
# twine upload dist/*
