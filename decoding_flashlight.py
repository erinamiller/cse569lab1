### pip3 install opencv-python
### pip3 install pillow
### pip3 install matplotlib
### pip3 install ckwrap
### pip3 install bcrypt

import cv2
import os
import ckwrap
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageStat

""" 
    Part 1. Identify Physical Signals.
"""

# Sources: https://theailearner.com/2018/10/15/extracting-and-saving-video-frames-using-opencv-python/

def video_to_images(input_video_dir, output_folder_dir):
    """
        Description: Convert input video to images of each frame and calculate 
                     the total number of frames in the input video.
        Input: 
            - input_video_dir: path of input video.
            - output_folder_path: the path of the folder that stores image of each frame.
        Output: 
            - Number of frames the input video generated (Return Value).
            - A folder that contains all frame images of the input video.
        Libraries you may need: 
            - cv2.VideoCapture()
            - os
    """
    # Your code starts here:
    # Use cv2 to open video, loop through each frame, and save frame to output_folder_dir
    video_object = cv2.VideoCapture(input_video_dir)
    i = 0
    while(video_object.isOpened()):
        ret, frame = video_object.read()
        if ret == False:
            break
        # cv2.imwrite(output_folder_dir + '/frame' + str(i) + '.jpg', frame)
        cv2.imwrite(output_folder_dir + 'frame' + str(i) + '.jpg', frame)
        i+=1

    return i


def brightness(im_file):
    """
        Description: Calculate the brightness of input image. 
        Input: 
            - im_file: path of the image.
        Output(Return Value): 
            - Return the brightness of input image.
        Libraries you may need: 
            - Image
            - ImageStat
    """
    # Your code starts here:
    # Open image with Image, convert image to greyscale to normalize brightness, and return average brightness
    # img = Image.open(im_file)
    # print(im_file)
    img = Image.open(im_file).convert('L')
    stat = ImageStat.Stat(img)
    return stat.mean[0]

def plot_brightness(x, y):
    """ Plot the brightness of each frame. """
    plt.figure(figsize=(15,5))
    plt.title('Brightness per Frame',fontsize=20)
    plt.xlabel(u'frame',fontsize=14)
    plt.ylabel(u'brightness',fontsize=14)
    plt.plot(x, y)
    plt.show()

""" 
    Part 2. Convert Physical Signals to Digital Signals.
"""

def brightness_to_lengths(threshold, brightness_per_frame):
    """
        Description: Calculate lengths of consistent signals.
        Input: 
            - threshold: a value of brightness that distinguishes light frames from dark ones.
            - brightness_per_frame: a list of brightness values of all frames.
        Output: 
            - A list of signal lengths (Return Value)
        Libraries you may need: N/A
    """
    # Your code starts here:
    # Iterate through brightness_per_frame, check if brightness greater or lesser than threshold
    # In each case, sub-case for incrementing counter or adding signal length to list and resetting counter
    signal_lengths = []
    counter = 0
    light_or_dark = False # True: light, False: dark
    for the_brightness in brightness_per_frame:
        # print(the_brightness)
        if the_brightness > threshold:
            # print("light")
            if light_or_dark == True:
                # Increment counter
                counter += 1
            else:
                # Was dark, now light
                signal_lengths.append(counter)
                counter = 0
                light_or_dark = True
        else:
            # print("dark")
            if light_or_dark == False:
                # Decrement counter
                counter -= 1
            else:
                # Was light, now dark
                signal_lengths.append(counter)
                counter = 0
                light_or_dark = False
    return signal_lengths

def classify_symbols(symbols):
    """
        Description: Due to the minor errors during the flashlight generating 
        and converting processes, the length of a symbol we calculate in 
        the last step is more likely to be a range than a certain value. 
        Implement the classify_symbols(symbols) function that labels 
        each length to a Morse symbol.
        Input: 
            - symbols: a list of signal lengths
        Output: 
            - A list of signal labels (Return Value)
        Libraries you may need: ckwrap.ckmeans
    """
    # Your code starts here:
    # Use ckwrap.ckmeans to cluster the signal lengths into groups
    result = ckwrap.ckmeans(symbols, 5)
    return result.labels

"""
    Part 3. Convert Morse Code to Plaintext
"""

morse_to_letter = {'.-':'A', '-...':'B', '-.-.':'C', '-..':'D', '.': 'E', '..-.':'F', '--.':'G',
                   '....':'H', '..':'I', '.---':'J', '-.-':'K', '.-..':'L', '--':'M', '-.':'N',
                   '---':'O', '.--.':'P', '--.-':'Q', '.-.':'R', '...':'S', '-':'T', 
                   '..-':'U', '...-':'V', '.--':'W', '-..-':'X', '-.--':'Y', '--..':'Z',
                   '.-.-.-':'.', '--..--':',', '-.-.--':'!', '..--..':'?', '-..-.':'/', '.--.-.':'@', '.----.':'\'',
                   '.----':'1', '..---':'2', '...--':'3', '....-':'4', '.....':'5',
                   '-....':'6', '--...':'7', '---..':'8', '----.':'9', '-----':'0'}

def morse_to_plaintext(morse):
    """
        Description: Convert Morse code to plaintext
        Input: 
            - morse: a list of labels, each label is a number that represents a kind of Morse Code.
              e.g. [3,2,3,1,4,2,3], where 
              0: space_between_words
              1: space_between_letters
              2: space_in_letter
              3: dot
              4: dash
        Output(Return Value): 
            - a plaintext sentence string
        Libraries you may need: N/A
    """
    # Your code starts here:
    # Iterate through morse, check if dot/dash/space/big space, and add corresponding letter
    # to letters based on morse_to_letter dictionary
    letters = []
    current_letter = ""
    for item in morse:
        if item == 3:
            # Dot
            current_letter = current_letter + "."
        elif item == 4:
            # Dash
            current_letter = current_letter + "-"
        elif item == 1:
            # Space between letters
            if len(current_letter) > 0:
                try:
                    letter = morse_to_letter[current_letter]
                    letters.append(letter)
                except:
                    print("Not a real letter :(")
                current_letter = ""
        elif item == 0:
            # Space between words
            if len(current_letter) > 0:
                try:
                    letter = morse_to_letter[current_letter]
                    letters.append(letter)
                except:
                    print("Not a real letter :(")
                current_letter = ""
                letters.append(" ")
    return letters

"""
    Part 4. Compile all above steps togther.
"""
def run(input_dir):
    # Part 1
    # output_name = input_dir.split('.')[0].split('/')[1]
    # output_dir = 'outputs/'+output_name+'_output'
    output_dir = "outputs/"
    # Your code starts here:
    num_images = video_to_images(input_dir, output_dir)

    print(" Checkpoint 1: brightness plot")
    brightnesses = []
    for i in range(num_images):
        brightnesses.append(brightness(output_dir + 'frame' + str(i) + '.jpg'))
    plot_brightness(range(num_images), brightnesses)
    
    # Part 2
    # Your code starts here:
    threshold = 140
    signals = brightness_to_lengths(threshold, brightnesses)
    classifications = classify_symbols(signals)
    print("Checkpoint 2: a labeled list of signal lengths is ", signals, classifications)

    # Part 3
    plaintext = morse_to_plaintext(classifications) # Your code starts here:
    print("Checkpoint 3: The plaintext is ", plaintext)
    return plaintext

def main():
    input_dir = 'inputs/encoded.mov'
    run(input_dir)

if __name__=="__main__":
    main()