## Why should you care?
Dungeons and Dragons (DnD) is a tabletop RPG game. It is very role play heavy, but you often have to roll a lot of dice to decide the outcome of certain actions. This can become tedious, and becomes even more so when you have to do math on the value of your roll. As you play more, you often get more math to do on your rolls. I for one am very slow at mental math and it can hinder the pace of what is going in the world you are playing in.
Imagine you are in the middle of a boss fight after weeks of build up. It is a titular moment, the Big Bad Evil Guy is about to fall, when all of the sudden you stop all momentum to add some silly numbers to your silly dice roll because, like me, you are bad at mental math. If you hate when this happens you only really have one option, use an online dice roller. You can set those up to do all of the math for you, but you miss out on the feeling of rolling a physical dice which is part of the fun of tabletop RPGs like DnD. This is where an auto dice detection tool comes into play. You get to roll an actual dice but have all of the math done for you.

## DISCLAIMER: It will NOT help you roll better!

## The Code Set Up
The pipeline depends on only a few common python packages
 - Numpy
 - Opencv
 - tkinter
Materials needed
 - Some dice
 - A flat colored background
 - A webcam
This does require some additional folder structure set up before running any code. You will need individual folders with reference images of each face of the dice you want to use. For example here are some of my 20 sided dice.

![tes5](https://github.com/user-attachments/assets/01810f4d-5256-426f-aa31-aeeb37539b35)
![test](https://github.com/user-attachments/assets/dd697289-6465-4912-b319-df297e7f5b64)

Be sure to take them with the camera that you will be using when you are detecting them, and also crop them as tight as you can. The latter helps make the vision system run faster.
	Because I the two main dice I want this to run are a 12 and 20 sided dice, I have my reference structure as follows

references
    |
    |-----d12
    |        |
    |        |---- all of my d12 reference pictures
    |
    |-----d20
    |        |
    |        |---- all of my d20 reference pictures
If you want to use a different naming scheme for your references, you will just need to change where they are used in the code. Otherwise use what is above and the system will work without needing to change anything.

The Physical Set Up
The main part of the physical set up is the camera. Depending on the webcam you are using you might be able to get away with more. For example, I tried leaving my webcam at the top of my monitor and tilting it down. The problem was that I had to zoom it in all the way and I lost a ton of resolution doing this. What I ended up doing was bring my camera lower, and setting the focus in the camera settings to ensure the dice was never out of focus.

![IMG_0946 (1)](https://github.com/user-attachments/assets/df462f05-3f8b-479b-b351-4d910cc4b25d)
This was the final version of the physical set up that doubled as a dice tower.

How It Works
	To start I have to give credit to this github repo https://github.com/Artefact2/autodice/tree/master. They used a really easily understood, and fast set up. The two main components are 1) image cropping and 2) reference matching.

Image Cropping
There are two main benefits to cropping the image; it lets the algorithm run faster as there are less pixels to look at, as well as it makes all of the information for the reference matching relevant. Meaning there is no extraneous pixel information in the image. The cropping starts with an edge detection. The image is taken and fed through opencv’s Canny function which applies Canny Edge detection (if you want to dig deeper here is their documentation https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html, but for this all we need to know is that it finds the edges). Once the edges are found we use opencv’s boundingRect function https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html . This essentially draws a box around the edges and we can use values of that box to crop the image using some numpy syntax.


![Screenshot 2024-11-13 100649](https://github.com/user-attachments/assets/7806580f-905d-45ca-8c5b-1b035ff6f5ce)

Here we can see the input image (top left) the edges (top right) and the final cropped image (bottom)

Reference Matching
The reference matching works by first feeding in all reference images into a sift keypoint detection algorithm https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html. Once all of that information is calculated we can do that same with the image of the dice we are trying to detect. We then use all of the keypoints and find the transformation matrix using homography. Homography gives us the matching points of each image. Since there could be “bad” points we only take the inliers, or “good” matches. The reference image with the most amount of inliers is assumed to be the correct dice face.

![Screenshot 2024-11-13 100800](https://github.com/user-attachments/assets/20b8e07e-c246-42c4-8d55-979b982fb4db)

The keypoints found (in red) and the inliers of those keypoints (red points with green lines)

How It All Comes Together
	The nice thing about knowing that the purpose of this is for online games, is that we know the user will be at their computer. With that we can make a little GUI to make our lives a bit easier. The basic flow is that you will roll your dice and then in the GUI select which dice you rolled. This will tell the system which reference file it should be looking at. Right now it displays the prediction in the terminal, but that will be changed to show in the GUI itself so that all of the interaction is self-contained in the GUI. The reason that I only have d12’s and d20’s set up is because those are the only two dice I ever have to do any math on. If you want to use other dice, just follow the set up steps above and create reference folders for those dice, and add additional buttons in the GUI for those dice by copy and pasting the button setup that is in there now. It is worth noting that you will likely need to manually adjust the zoom and focus of your camera to get consistent results.
 
![Screenshot 2024-11-13 100829](https://github.com/user-attachments/assets/b82954d5-1474-4b85-9e86-cb2a80ecab2d)

The GUI on the left was the initial prototype while the right is the final version.

Extendability
	Expanding on this idea is important as, right now, it is only set up for what I need it to do. For example, all of the three checks apply different values to the dice roll and might only be applicable to my character, for another person’s character they may need different checks or even different dice. I will focus on the flow from generating the reference images to adding a button in the GUI for them, as all the camera stuff should remain the same between dice. Some background information on the tkinter library, the general structure is you create an object and then you “pack” it into the defined frame.

Step 1: Collecting reference images
	To start collecting new reference images for you dice, find these lines of code in the run_GUI_v2() function and uncomment them;
 
 ![Screenshot 2024-11-13 100917](https://github.com/user-attachments/assets/94b7f7d4-8fa2-478b-9714-6f2d9dc09c9d)

This will add a “save ref” button to the GUI. You will need to change the filepath in the save_img() function in the “command” argument to correspond to the location and dice number you are saving, this must be done for any new dice being saved. Then, all you need to do is work through the GUI and press the “save ref” button on each dice race. MAKE SURE you take the reference images in order from one to the max dice face. You will need to restart if you go out of order, or take new references for new dice.

Step 2: Adding a button

![Screenshot 2024-11-13 100937](https://github.com/user-attachments/assets/5d867289-e750-4d57-afd5-3d02b3ee3de3)

This image will be the reference for the rest of this section.

Starting at the top of the image, use tk.Button to create a new button. The “buttonFrame” variable doesn’t matter but if you want to learn more you can google “Tkinter frames”, they let you define different subsections in the display. To make the button do something we set a function in the “command” argument. Here we are using “roll_d20()”, because it is the d20 button. Skipping over the “roll_d20()” function for now, the next two lines with “gwm” and “GWM” define the check boxes seen in the GUI, again you can make this whatever you like. These are followed by the “pack()” we saw earlier. Going back up to “roll_d20()” we will see how to add any check values to our roll. We first pull the value of the checkbox and use our “better_dice_roll” function (the “dice_type” should be the name of the folder within the “references” directory defined earlier). We can then start adding values to the roll based on the condition of the GWM checkbox. Finally we output it to the text box. Many of the variables seen that aren’t defined in the screen shot are global variables that can be changed to anything, just change them and their values and add them to functions like “roll_d20()” whenever you need to.

Short Story Time:
So I did use this the last DnD session I had and it was super nice to not have to do any math, but I proceeded to roll incredibly poorly. I think I only rolled above five 3 times over the course of three hours. So while this does work and is, in my opinion, very cool, it will not help you roll better!

![Screenshot 2024-11-13 101009](https://github.com/user-attachments/assets/20f34c1d-73ec-4066-a009-b3c5c6b84e20)

This is what it looks like when you roll
