import cv2
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

import tkinter as tk

def dice_roll(ref_images_path, query_image):
    highest_score = 0
    image = ""
    # ref_images_path = "references/d12-v3"
    # query_image = "test_inputs/d12-v2/4.jpg"
    for i in tqdm(os.listdir(ref_images_path)):
        img1 = cv2.imread(os.path.join(ref_images_path, i), cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(query_image, cv2.IMREAD_GRAYSCALE)
        
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
    window.geometry("500x500")
    window.title("DnD calculate dice roll")

    

    d_12_roll = tk.Button(
    text="d12 Roll",
    width=10,
    height=5,
    command=lambda: dice_roll("references/d12-v3")
    )
    d_20_roll = tk.Button(
        text="d20 Roll",
        width=10,
        height=5,
        command=lambda: dice_roll("references/d20")
    )
    d_12_roll.pack()
    d_20_roll.pack()



    
    window.mainloop()
    print("here")

if __name__ == "__main__":
    run_GUI()
    exit(0)

    cap = cv2.VideoCapture(0)



    ret, frame = cap.read()
    cv2.imshow("Webcam", frame)
    cv2.waitKey(0)



    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()