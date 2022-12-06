# SCTG - SCREENSHOT TAG 
A cross-platform [YOLO](https://github.com/AlexeyAB/darknet) enhanced, tagging, screenshot app that tags\\stores detected objects within image's EXIF's UserComment entry. `ALPHA VERSION 0.1.0`

# Setup
```terminal
git clone https://github.com/GiorgosXou/SCTG && cd SCTG
```
```terminal
pip install .
```


# Usage
```terminal
sctg ~/my_screenshot_folder
```

| Print Screen +   | Description |
|     ----         |    -----    |
|                  | Screenshot |
|    ctrl          | Screenshot Cut Area |
|    shift         | Screenshot Without Saving |
|    ctrl + shift  | Screenshot Cut Area dont save |

* right click on screenshot to add extra tags
* Copy to clipboard is not yet supported for mac and windows
* To search for tags in images install [`exiftool`](https://exiftool.org/) for example in arch:
```terminal
sudo pacman -S perl-image-exiftool
```
and then use `grep` or something to find what you want, like:
```terminal
exiftool * -UserComment | grep -i YouTube
```


# Tested
Tested, on Arch linux with i3 btw 🤓

# Disclaimer
This is just a crappy implementation of a nice idea that i had. Don't get anything at this alpha version too seriously

# Outro
If you use linux you might need to install libnotify too. here's a silly screenshot example, have a look up right:

<img title="a title" alt="Alt text" src="./sctg_2022-12-06 02:58:31.587667.jpg">
