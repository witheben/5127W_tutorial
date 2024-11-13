import cv2
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm
from PIL import Image
from PIL import ImageTk
import glob

import tkinter as tk

from autodice import *


rage_bonus = 2
strength_bonus = 6
prof_bonus = 4
weapon_bonus = 1

cv2image = None
frame = None


'''
better_dice_roll
    inputs:
        - dice_type: the name of the folder in the "references" directory to look for matches in
        - query_image: the image to do the comparison with
    outputs:
        - roll_value: the detected value of the dice
'''
def better_dice_roll(dice_type, query_image):
    '''
    1. Autocrop the query image
    2. Calculate the reference image keypoints
    3. Calculate the best score 
    '''
    start_time = time.time()
    input_img = query_image
    #1
    cropped_input_query = autocrop(input_img)
    #2
    refdata = dict()
    for reffile in glob.glob('references/{}/*.jpg'.format(dice_type)):
        i = reffile.split('/')[-1].split('.')[0]
        
        img = cv2.imread(reffile, -1)
        print(img.shape)
        refdata[i] = (
            keypointsAndDescriptors(img),
            img,
        )
    #3
    final_result = refmatch(cropped_input_query, refdata)
    end_time = time.time()

    roll_value = final_result.split("d")[-1].split("_")[0]

    print("predicted dice roll on a {}: {}".format(dice_type, final_result))
    print("Finished in {} seconds".format((round((end_time-start_time), 2))))
    return roll_value

'''
save_img
    inputs:
        - save_dir: directory to save the frames into
        - input_image: the image to save 
    outputs:
        - none
'''
dice_number = 1
def save_img(save_dir, input_image):
    global dice_number
    cropped_input_query = autocrop(input_image)
    cv2.imshow('test', cropped_input_query)
    cv2.waitKey(0)
    print(save_dir)
    cv2.imwrite("{}/d{}_v2.jpg".format(save_dir, dice_number), cropped_input_query)
    dice_number += 1



'''
Runs the GUI and controls all of the button logig
'''
def run_GUI_v2():
    window = tk.Tk()
    window.geometry("900x550")
    window.title("DnD calculate dice roll")

    # Graphics window - this sets up the frame in Tkinter that contains the video feed
    imageFrame = tk.Frame(window, width=500, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    #Capture video frames
    lmain = tk.Label(imageFrame)
    # lmain.grid(row=0, column=0)
    lmain.pack()
    cap = cv2.VideoCapture(0)
    
    # this controls the logic for displaying the video feed in Tkinter
    # the only thing worth noting is that the frame is stored in a global variable to make it available to other function
    def show_frame():
        global cv2image
        global frame
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame) 
    

    # Sets up the second frame in tkinter that contains the buttons and checkboxes
    buttonframe = tk.Frame(window, width=500, height=500)
    buttonframe.grid(row=0, column=1)

    # button setup
    d_12_roll = tk.Button(buttonframe,
        text="d12 Roll",
        width=10,
        height=5,
        bg='#22631b',
        command=lambda: roll_d12()
    )

    # function that the button above calls
    def roll_d12():
        GWM = gwm.get()
        rage = RAGE.get()
        damage_value = int(better_dice_roll(dice_type="d12-v4", query_image=frame))
        damage_value = damage_value + 10 if GWM else damage_value
        damage_value = damage_value + rage_bonus if rage else damage_value
        damage_value += strength_bonus
        

    d_20_roll = tk.Button(buttonframe,
        text="d20 Roll",
        width=10,
        height=5,
        bg='#756a22',
        command=lambda: roll_d20()
    )
    


    def roll_d20():
        GWM = gwm.get()
        attack_value = int(better_dice_roll(dice_type="d20-v2", query_image=frame))
        attack_value = attack_value - 5 if GWM else attack_value
        attack_value += strength_bonus + weapon_bonus + prof_bonus
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.INSERT, f"{attack_value}")
        return

    
    # checkbox set up
    gwm = tk.BooleanVar()
    rage = tk.BooleanVar()
    GWM = tk.Checkbutton(buttonframe, text="Using GWM?", variable=gwm, onvalue=True, offvalue=False)
    RAGE = tk.Checkbutton(buttonframe, text="Raging?", variable=rage, onvalue=True, offvalue=False)
    
    roll_label = tk.Label(buttonframe, text="Result from the roll and math!")
    result_text = tk.Text(buttonframe,
                          width=3,
                          height=1,
                          font=('Helvetica', 32))
    # packs the buttons in the frame, the ordering looks odd here, but it forces them into the right place when running
    d_12_roll.pack()
    d_20_roll.pack()

    '''
    uncomment out to add a button for adding reference images
    '''
    # save_frame = tk.Button(buttonframe,
    #     text="save ref",
    #     width=10,
    #     height=5,
    #     command=lambda: save_img("references/d20-v2", frame)
    # )
    # save_frame.pack()

    GWM.pack()
    RAGE.pack()
    roll_label.pack()
    result_text.pack()

    show_frame()
    window.mainloop()


if __name__ == "__main__":

    run_GUI_v2()
    