
# pip3 install piexif
# Python program to take
# screenshots

import pyautogui
import numpy        as np
import sys
import os
import cv2
import piexif
import traceback
import sctg.globals
from   pynput.mouse import Controller
from   notifypy     import Notify     
from   pynput       import keyboard
from   PIL          import Image
from   .cpimg       import copy_image
from   .gfwin       import get_focused_window
from   .EditWindow  import EditWindow
from   datetime     import datetime as dt


mouse = Controller()
nc    = Notify    ()
CURRENT_PATH     = os.path.dirname(__file__)
CRITICAL_ICON    = f'{CURRENT_PATH}/icons/5124639571624510123.svg'
SCTG_PATH        = ''
KEY_PRINT_SCREEN = keyboard.Key.print_screen #personally i like to use f2 too

def send_notification(title, message='', urgency='normal', icon=''):
    nc.urgency = urgency
    nc.title   = title
    nc.message = message
    nc.icon    = icon
    nc.send()


CONFIDENCE      = 0.5
SCORE_THRESHOLD = 0.5
IOU_THRESHOLD   = 0.5
config_path     = f"{CURRENT_PATH}/nn_files/yolov7-tiny.cfg"                           # the neural network configuration
weights_path    = f"{CURRENT_PATH}/nn_files/yolov7-tiny.weights"                       # the YOLO net weights file
labels          = open(f"{CURRENT_PATH}/nn_files/coco.names").read().strip().split("\n") # loading all the class labels (objects)
net             = cv2.dnn.readNetFromDarknet(config_path, weights_path) # load the YOLO network

def detect(image): # 1 -> references from where i stole the code at the bottom of the file
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False) # create 4D blob
    net.setInput(blob) # sets the blob as the input of the network
    ln = net.getLayerNames() # get all the layer names
    try:               ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    except IndexError: ln = [ln[i    - 1] for i in net.getUnconnectedOutLayers()] #in case getUnconnectedOutLayers() returns 1D array when CUDA isn't available
    layer_outputs = net.forward(ln) # feed forward (inference) and get the network output
    objs, boxes, confidences, class_ids = [], [], [], []
    for output in layer_outputs: # loop over each of the layer outputs
        for detection in output: # loop over each of the object detections
            scores     = detection[5:] # extract the class id (label) and confidence (as a probability) of the current object detection
            class_id   = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > CONFIDENCE: # discard out weak predictions by ensuring the detected probability is greater than the minimum probability
                box = detection[:4] * np.array([w, h, w, h]) # scale the bounding box coordinates back relative to the size of the image, keeping in mind that YOLO actually returns the center (x, y)-coordinates of the bounding box followed by the boxes' width and height
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width  / 2)) # use the center (x, y)-coordinates to derive the top and and left corner of the bounding box
                y = int(centerY - (height / 2))
                boxes.append([x, y, int(width), int(height)]) # update our list of bounding box coordinates, confidences, and class IDs
                confidences.append(float(confidence))
                class_ids.append(class_id)
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD) # perform the non maximum suppression given the scores defined before
    if len(idxs) > 0:
        objs.extend(['yolov7', len(idxs)])
        for i in idxs.flatten(): # loop over the indexes we are keeping
            objs.extend([labels[class_ids[i]], format(confidences[i], '.3f')])
    return objs 


def init_edit_window(image):
    win   = EditWindow(image)
    win.mainloop()
    img = win.image
    win.destroy()
    return img


def screenshot(area=False, save=True, silent=False): # https://stackoverflow.com/a/63400376/11465149
    name      = f'sctg_{dt.now()}.jpg'
    img       = pyautogui.screenshot()
    ms        = [mouse.position]
    gfw       = get_focused_window()
    if area: 
        image = init_edit_window(img)
        if image == None: 
            sctg.globals.InputFrmTXT = ''# lol this shit feels so wrong xD
            return
        image = np.array(image)
    else:
        image = np.array(img)
    objs      = detect(image)
    tags      = f"#{gfw.split() + sctg.globals.InputFrmTXT.split() + objs + ms}" 
    sctg.globals.InputFrmTXT = ''# Not clearing InputFrmTxT might be a feauture lol xD
    data      = bytes(tags,'utf-8') #pickle.dumps(tags)
    exif_ifd  = {piexif.ExifIFD.UserComment: data}
    exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {}, "thumbnail": None, "GPS": {}}
    img       = Image.fromarray(image)
    exif_dat  = piexif.dump(exif_dict)
    img.save(f'{SCTG_PATH}/{name}',  exif=exif_dat) # exiftool * -UserComment | grep -i YouTube
    copy_image(f'{SCTG_PATH}/{name}')
    if not save: # lol whatever
        os.remove(f'{SCTG_PATH}/{name}')
    if not silent: send_notification(f"{name}", tags) 


ctrl = False # Because for some reason hotkey doesnt seem to work lol
shift  = False 
def on_key_release(key):
    global ctrl, shift
    ctrl  = False
    shift = False



def on_key_press(key):
    global ctrl, shift
    if   key == KEY_PRINT_SCREEN and ctrl and shift : screenshot(area=True, save=False)
    elif key == KEY_PRINT_SCREEN and ctrl           : screenshot(area=True            )
    elif key == KEY_PRINT_SCREEN and shift          : screenshot(save=False           ) 
    elif key == KEY_PRINT_SCREEN                    : screenshot()
    elif key == keyboard.Key.ctrl                   : ctrl  = True
    elif key == keyboard.Key.shift                  : shift = True


def main():
    if len(sys.argv) == 1:
        send_notification('Error: No screenshot folder', 'There was no folder specified for screenshots', 'critical', CRITICAL_ICON)
        exit()
    global SCTG_PATH
    SCTG_PATH = sys.argv[1]
    if not os.path.isdir(SCTG_PATH):
        send_notification('Folder not found', f"'{SCTG_PATH}' is not a directory", 'critical', CRITICAL_ICON)
        exit()

    try:
        with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener: listener.join()
    except:
        send_notification('Error', traceback.format_exc(), 'critical', CRITICAL_ICON)


if __name__ == '__main__':        
    main()



"""
# 1
- https://www.thepythoncode.com/article/yolo-object-detection-with-opencv-and-pytorch-in-python
- https://github.com/AlexeyAB/darknet/tree/master/cfg
- https://github.com/AlexeyAB/darknet/releases

# Other
- https://practicaldatascience.co.uk/data-science/how-to-use-image-hashing-to-identify-visually-similar-or-duplicate-images
- https://stackoverflow.com/questions/2661778/tag-generation-from-a-text-content
"""
