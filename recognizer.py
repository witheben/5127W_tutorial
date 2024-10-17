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

cv2image = None


def better_dice_roll(dice_type, query_image):
    '''
    1. Autocrop the query image
    2. Calculate the reference image keypoints
    3. Calculate the best score 
    '''
    start_time = time.time()
    input_img = cv2.imread(query_image)
    #1
    cropped_input_query = autocrop(input_img)
    #2
    refdata = dict()
    for reffile in glob.glob('references/{}/*.jpg'.format(dice_type)):
        i = reffile.split('/')[-1].split('.')[0]
        img = cv2.imread(reffile, -1)
        refdata[i] = (
            keypointsAndDescriptors(img),
            img,
        )
    #3
    final_result = refmatch(cropped_input_query, refdata)
    end_time = time.time()
    print("predicted dice roll on a {}: {}".format(dice_type, final_result))
    print("Finished in {} seconds".format((round((end_time-start_time), 2))))



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
    window.geometry("500x1000")
    window.title("DnD calculate dice roll")

    # #Graphics window
    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    #Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    cap = cv2.VideoCapture(0)
    
    def show_frame():
        global cv2image
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
        # cv2.imshow('win', cv2image)
        # cv2.waitKey(0)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame) 
    

    d_12_roll = tk.Button(
    text="d12 Roll",
    width=10,
    height=5,
    command=lambda: dice_roll("references/d12-v3", cv2image)
    )
    d_20_roll = tk.Button(
        text="d20 Roll",
        width=10,
        height=5,
        command=lambda: dice_roll("references/d20", cv2image)
    )
    d_20_roll.grid(row=2, column=1)
    d_12_roll.grid(row=1, column=1)
    # d_12_roll.pack()
    # d_20_roll.pack()



    show_frame()
    window.mainloop()
    print("here")

if __name__ == "__main__":
    better_dice_roll(dice_type="d12-v3", query_image="test_inputs/d12-v2/10.jpg")
    exit(0)
    run_GUI()
    

    cap = cv2.VideoCapture(0)



    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)
    cv2.waitKey(0)



    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()