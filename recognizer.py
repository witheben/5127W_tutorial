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


def better_dice_roll(dice_type, query_image):
    '''
    1. Autocrop the query image
    2. Calculate the reference image keypoints
    3. Calculate the best score 
    '''
    start_time = time.time()
    # input_img = cv2.imread(query_image)
    input_img = query_image
    #1
    cropped_input_query = autocrop(input_img)
    # print(input_img.shape)
    # print(input_img[0])
    #2
    refdata = dict()
    for reffile in glob.glob('references/{}/*.jpg'.format(dice_type)):
        i = reffile.split('/')[-1].split('.')[0]
        
        img = cv2.imread(reffile, -1)
        # cv2.imshow("idk", img)
        # cv2.waitKey(0)
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

dice_number = 1
def save_img(save_dir, input_image):
    global dice_number
    cropped_input_query = autocrop(input_image)
    # print(input_img.shape)
    cv2.imshow('test', cropped_input_query)
    cv2.waitKey(0)
    print(save_dir)
    cv2.imwrite("{}/d{}_v2.jpg".format(save_dir, dice_number), cropped_input_query)
    dice_number += 1



def dice_roll(ref_images_path, query_image):
    highest_score = 0
    image = ""
    # ref_images_path = "references/d12-v3"
    # query_image = "test_inputs/d12-v2/4.jpg"
    img2 = query_image
    for i in tqdm(os.listdir(ref_images_path)):
        img1 = cv2.imread(os.path.join(ref_images_path, i), cv2.IMREAD_GRAYSCALE)
        # img2 = cv2.imread(query_image, cv2.IMREAD_GRAYSCALE)
        
        # Initiate ORB detector
        orb = cv2.ORB_create()
        
        # find the keypoints and descriptors with ORB
        kp1, des1 = orb.detectAndCompute(img1,None)
        kp2, des2 = orb.detectAndCompute(img2,None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        # Match descriptors.
        matches = bf.match(des1,des2)
        
        # # Sort them in the order of their distance.
        # matches = sorted(matches, key = lambda x:x.distance)
        
        # # Draw first 10 matches.
        # img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        if len(matches) > highest_score:
            highest_score = len(matches)
            image = i
        # print()
        # print(i)
        # print(len(matches))
        # plt.imshow(img3),plt.show()
    print(highest_score)
    print(image)

def run_GUI():
    window = tk.Tk()
    window.geometry("665x1000")
    window.title("DnD calculate dice roll")

    # #Graphics window
    imageFrame = tk.Frame(window, width=500, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    #Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    cap = cv2.VideoCapture(0)
    
    def show_frame():
        global cv2image
        global frame
        _, frame = cap.read()
        # print(1)
        # print(frame.shape)
        frame = cv2.flip(frame, 1)
        # print(frame.shape)
        cv2image = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        # print(cv2image.shape)
        # cv2image = cv2.resize(cv2image, (500, 500))
        # cv2.imshow('win', cv2image)

        # cv2.waitKey(0)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame) 
    
    # better_dice_roll(dice_type, query_image):
    d_12_roll = tk.Button(
    text="d12 Roll",
    width=10,
    height=5,
    bg='#22631b',
    command=lambda: better_dice_roll(dice_type="d12-v4", query_image=frame)
    )
    # d_12_roll = tk.Button(
    # text="d12 Roll",
    # width=10,
    # height=5,
    # command=lambda: dice_roll("references/d12-v3", cv2image)
    # )
    d_20_roll = tk.Button(
        text="d20 Roll",
        width=10,
        height=5,
        bg='#756a22',
        command=lambda: better_dice_roll(dice_type="d20-v2", query_image=frame)
    )
    # d_20_roll = tk.Button(
    #     text="d20 Roll",
    #     width=10,
    #     height=5,
    #     command=lambda: dice_roll("references/d20", cv2image)
    # )

    # save_frame = tk.Button(
    #     text="save ref",
    #     width=10,
    #     height=5,
    #     command=lambda: save_img("references/d20-v2", frame)
    # )
    d_12_roll.grid(row=1, column=0, sticky='nsew')
    d_20_roll.grid(row=2, column=0, sticky="nsew")
    # save_frame.grid(row=2, column=0)



    show_frame()
    window.mainloop()

def run_GUI_v2():
    window = tk.Tk()
    window.geometry("900x550")
    window.title("DnD calculate dice roll")

    # #Graphics window
    imageFrame = tk.Frame(window, width=500, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    #Capture video frames
    lmain = tk.Label(imageFrame)
    # lmain.grid(row=0, column=0)
    lmain.pack()
    cap = cv2.VideoCapture(0)
    
    def show_frame():
        global cv2image
        global frame
        _, frame = cap.read()
        # print(1)
        # print(frame.shape)
        frame = cv2.flip(frame, 1)
        # print(frame.shape)
        cv2image = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        # print(cv2image.shape)
        # cv2image = cv2.resize(cv2image, (500, 500))
        # cv2.imshow('win', cv2image)

        # cv2.waitKey(0)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame) 
    

    buttonframe = tk.Frame(window, width=500, height=500)
    buttonframe.grid(row=0, column=1)
    # better_dice_roll(dice_type, query_image):
    d_12_roll = tk.Button(buttonframe,
    text="d12 Roll",
    width=10,
    height=5,
    bg='#22631b',
    command=lambda: better_dice_roll(dice_type="d12-v4", query_image=frame)
    )
    # d_12_roll = tk.Button(
    # text="d12 Roll",
    # width=10,
    # height=5,
    # command=lambda: dice_roll("references/d12-v3", cv2image)
    # )
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
        print(attack_value)
        attack_value = attack_value - 5 if GWM else attack_value
        attack_value += strength_bonus + weapon_bonus + prof_bonus
        print(attack_value)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.INSERT, f"{attack_value}")
        return

    gwm = tk.BooleanVar()
    rage = tk.BooleanVar()
    svge = tk.BooleanVar()
    GWM = tk.Checkbutton(buttonframe, text="Using GWM?", variable=gwm, onvalue=True, offvalue=False)
    RAGE = tk.Checkbutton(buttonframe, text="Raging?", variable=rage, onvalue=True, offvalue=False)
    SAVAGE_ATTACK = tk.Checkbutton(buttonframe, text="Savage Attack?", variable=svge, onvalue=True, offvalue=False)
    
    roll_label = tk.Label(buttonframe, text="Result from the roll and math!")
    result_text = tk.Text(buttonframe,
                          width=3,
                          height=1,
                          font=('Helvetica', 32))

    d_12_roll.pack()
    d_20_roll.pack()

    GWM.pack()
    RAGE.pack()
    SAVAGE_ATTACK.pack()
    roll_label.pack()
    result_text.pack()


    # save_frame.grid(row=2, column=0)



    show_frame()
    window.mainloop()


if __name__ == "__main__":
    # better_dice_roll(dice_type="d12-v3", query_image="test_inputs/d12-v2/10.jpg")
    # exit(0)
    # run_GUI()
    run_GUI_v2()
    

    # cap = cv2.VideoCapture(0)



    # ret, frame = cap.read()
    # cv2.imshow("Webcam", frame)
    # cv2.waitKey(0)



    # Release the camera and close the window
    # cap.release()
    # cv2.destroyAllWindows()