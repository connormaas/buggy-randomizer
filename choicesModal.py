################################################################################ 
#####################            CHOICES MODAL           #######################
################################################################################
'''
Note that is this "modal" is actually just a canvas on top of the window, but
it acts like a modal
'''
import random
from tkinter import *
from PIL import ImageTk, Image
from scheduleDocuments import ScheduleDocuments
import constants

class ChoicesModal:
    def __init__(self, window):
        # set winow and create "modal" canvas
        self.window = window
        self.modal = Canvas(
            self.window, width=1100, height=550, bg=constants.BACKGROUND, bd=0, 
            highlightthickness=5
        )
        self.modal.place(
            x=constants.WIDTH / 2, y=constants.HEIGHT / 2 + 50, anchor="center"
        )

        # initialize button that finishes the animation process immediately
        self.modal.finish = False
        finishButton = Button(
            self.window, text="Finish Animation", 
            highlightbackground=constants.BACKGROUND, bd=0, 
            command=(lambda: setattr(self.modal, 'finish', True))
        )
        self.finishButtonWindow = self.modal.create_window(
            1095, 545, anchor="se", window=finishButton
        )

        # set some inital values for our position displays and logic
        self.flaggersList = []
        self.pushersList = []
        self.backupsList = []
        self.barricadersList = []
        self.balesList = []
        self.videoTimersList = []
        self.displayPushers = self.modal.create_text(
            10, 10, anchor="nw", text="Pusher: " + "N/A", font=("Arial", 15), 
            fill="White"
        )
        self.displayFlaggers = self.modal.create_text(
            10, 45, anchor="nw", text="Flaggers: " + "N/A", font=("Arial", 15), 
            fill="White"
        )
        self.displayVideoTimers = self.modal.create_text(
            10, 80, anchor="nw", text="Video & Timers: " + "N/A", 
            font=("Arial",15), fill="White"
        )
        self.displayBales = self.modal.create_text(
            10, 115, anchor="nw", text="Bales: " + "N/A", font=("Arial", 15), 
            fill="White"
        )
        self.displayBarricaders = self.modal.create_text(
            10, 150, anchor="nw", text="Barricaders: " + "N/A", 
            font=("Arial", 15), fill="White"
        )
        self.displayBackups = self.modal.create_text(
            10, 185, anchor="nw", text="Backups: " + "N/A", font=("Arial", 15), 
            fill="White"
        )

    def __resizeAndCrop(self, img, size):
        '''
        Resize our [img] based on [size] and crop into into a square
        '''
        (width, height) = img.size
        # Determine the size of the square side
        sizer = min(width, height)
        
        # Calculate cropping coordinates to get a centered square
        left = (width - sizer) / 2
        top = (height - sizer) / 2
        right = (width + sizer) / 2
        bottom = (height + sizer) / 2
        
        # Crop the image to a square
        tmp = img.crop((left, top, right, bottom))
        
        # Scale image to the given size
        return ImageTk.PhotoImage(tmp.resize((size, size), Image.LANCZOS))

    def __spin(self, images, t, x, y):
        '''
        Quickly swaps between randomized list of [images], creating a spinning
        effect
        '''
        self.waithere(t)
        random.shuffle(images)
        for i in range(0, 8):
            img = self.modal.create_image(
                x, y, anchor = "center", image=images[i]
            )
            self.waithere(250)
            if self.modal.finish:
                self.modal.delete(img)
                break
            self.modal.delete(img)

    def __produceLines(self, L, n):
        '''
        General function which takes in list of strings [L] and a maxiumum 
        character length per line [n]. Returns a string joined by commas with 
        new lines inserted when the character limit is reached
        '''
        result = ""
        totalChars = 0
        for name in L:
            if L.index(name) == len(L) - 1:
                end = ""
            else:
                end = ", "
            prevChars = totalChars
            totalChars = totalChars + len(name)
            if (totalChars % n) < (prevChars % n):
                result = result + "\n" + name + end
            else:
                result = result + name + end
        return result

    def __getNameFromPath(self, path):
        '''
        Given a path of the from 'image/A.png', we get A
        '''
        return (path.removeprefix("images/")).removesuffix(".png")

    def __displayNext(self, requiredNumbers, pathsChosen, i):
        '''
        Updates the display depending on our index in [pathsChosen] ([i]) in 
        comparison to [requiredNumbers]. It return the position associated with
        this location
        '''
        if i < (requiredNumbers["pushers"]):
            position = "Pusher"
            self.pushersList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayPushers)
            pushersText = (
                "Pushers: " + self.__produceLines(self.pushersList, 105)
            )
            self.displayPushers = self.modal.create_text(
                10, 10, anchor="nw", text=pushersText, font=("Arial", 15), 
                fill="White"
            )
        elif i < requiredNumbers["pushers"] + requiredNumbers["flaggers"]:
            position = "Flagger"
            self.flaggersList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayFlaggers)
            flaggersText = (
                "Flaggers: " + self.__produceLines(self.flaggersList, 105)
            )
            self.displayFlaggers = self.modal.create_text(
                10, 45, anchor="nw", text=flaggersText, font=("Arial", 15), 
                fill="White"
            )
        elif i < (
                requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                requiredNumbers["videotimers"]
            ):
            position = "Video & Timer"
            self.videoTimersList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayVideoTimers)
            videoTimerText = (
                "Video & Timers: " + self.__produceLines(self.videoTimersList, 105)
            )
            self.displayVideoTimers = self.modal.create_text(
                10, 80, anchor="nw", text=videoTimerText, font=("Arial", 15), 
                fill="White"
            )
        elif i < (
                requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                requiredNumbers["videotimers"] + requiredNumbers["bales"]
            ):
            position = "Bales"
            self.balesList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayBales)
            balesText = (
                "Bales: " + self.__produceLines(self.balesList, 120)
            )
            self.displayBales = self.modal.create_text(
                10, 115, anchor="nw", text=balesText, font=("Arial", 15), 
                fill="White"
            )
        elif i < (
                requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                requiredNumbers["videotimers"] + requiredNumbers["bales"] + 
                requiredNumbers["barricaders"]
            ):
            position = "Barricaders"
            self.barricadersList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayBarricaders)
            barricadersText = (
                "Barricaders: " + 
                self.__produceLines(self.barricadersList,120)
            )
            self.displayBarricaders = self.modal.create_text(
                10, 150, anchor="nw", text=barricadersText, font=("Arial", 15), 
                fill="White"
            )
        else:
            position = "Backups"
            self.backupsList.append(self.__getNameFromPath(pathsChosen[i]))
            self.modal.delete(self.displayBackups)
            backupsText = "Backups: " + self.__produceLines(self.backupsList, 120)
            self.displayBackups = self.modal.create_text(
                10, 185, anchor="nw", text=backupsText, font=("Arial", 15), 
                fill="White"
            )

        return position

    def __finalizeLists(self, pathsChosen, requiredNumbers):
        '''
        In case the playSelections animations are ended early, this function 
        goes back and updates the lists based on the orignal selections to be 
        displayed on the final screen. If there are no people in a position, 
        "N/A" is added to the list for that position
        '''
        self.pushersList = []
        self.flaggersList = []
        self.videoTimersList = []
        self.balesList = []
        self.barricadersList = []
        self.backupsList = []

        for i in range(len(pathsChosen)):
            if i < requiredNumbers["pushers"]:
                self.pushersList.append(self.__getNameFromPath(pathsChosen[i]))
            elif i < requiredNumbers["pushers"] + requiredNumbers["flaggers"]:
                self.flaggersList.append(self.__getNameFromPath(pathsChosen[i]))
            elif i < (
                    requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                    requiredNumbers["videotimers"]
                ):
                self.videoTimersList.append(
                    self.__getNameFromPath(pathsChosen[i])
                )
            elif i < (
                    requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                    requiredNumbers["videotimers"] + requiredNumbers["bales"]
                ):
                self.balesList.append(self.__getNameFromPath(pathsChosen[i]))
            elif i < (
                    requiredNumbers["pushers"] + requiredNumbers["flaggers"] + 
                    requiredNumbers["videotimers"] + requiredNumbers["bales"] 
                    + requiredNumbers["barricaders"]
                ):
                self.barricadersList.append(
                    self.__getNameFromPath(pathsChosen[i])
                )
            else:
                self.backupsList.append(self.__getNameFromPath(pathsChosen[i]))
        
        if len(self.pushersList) == 0:
            self.pushersList.append("N/A")
        if len(self.flaggersList) == 0:
            self.flaggersList.append("N/A")
        if len(self.videoTimersList) == 0:
            self.videoTimersList.append("N/A")
        if len(self.balesList) == 0:
            self.balesList.append("N/A")
        if len(self.barricadersList) == 0:
            self.barricadersList.append("N/A")
        if len(self.backupsList) == 0:
            self.backupsList.append("N/A")
    
    def __createAndEmailDocuments(self, choicesDict, date, emailAddresses):
        '''
        This function handles creating and emailing docx files based on the 
        generated positions. It uses the custom library scheduleDocuments
        '''
        doc = ScheduleDocuments(date)
        files = doc.create(choicesDict)
        doc.email(emailAddresses, files)

    def __playSelections(
            self, pathsChosen, imagesChosen, imagesAll, requiredNumbers
        ): 
        '''
        This function handles the animations for the chosen members. It displays 
        a "spinning animation" for each chosen member assigning them to a 
        specific positon. It also displays running lists for the members that
        have been assigned to specific positions.
        '''
        for i in range(len(pathsChosen)):
            # exit animations if requested
            if self.modal.finish:
                break
            # perform our spin animation
            self.__spin(imagesAll, 0, constants.MODALMIDX, 395)
            # exit animations if requested
            if self.modal.finish:
                break

            # update our display
            position = self.__displayNext(requiredNumbers, pathsChosen, i)
            img = self.modal.create_image(
                constants.MODALMIDX, 395, anchor="center", image=imagesChosen[i]
            )
            text = self.modal.create_text(
                constants.MODALMIDX, 375 + (constants.PICSIZE / 2) - 7, 
                text=position.upper(), font=("Trattatello", 30), 
                fill=constants.GARNET
            )
            bbox = self.modal.bbox(text)
            background = self.modal.create_rectangle(
                bbox[0] - constants.PICSIZE / 2 + (bbox[2] - bbox[0]) / 2, 
                bbox[1], 
                bbox[2] +  constants.PICSIZE / 2 - (bbox[2] - bbox[0]) / 2, 
                bbox[3], outline="", fill="White"
            )
            self.modal.tag_lower(background, text)

            # display the result for 2.5 seconds
            self.waithere(2500)
            self.modal.delete(img)
            self.modal.delete(text)
            self.modal.delete(background)
            
            # exit animations if requested
            if self.modal.finish:
                break

    def __displayFinal(self):
        '''
        This displays the final screen after the animations complete, including 
        the section allowing you to create a schedule document and email it
        '''
        # clear everything currently on the screen
        self.modal.delete(self.displayFlaggers)
        self.modal.delete(self.displayPushers)
        self.modal.delete(self.displayBackups)
        self.modal.delete(self.displayVideoTimers)
        self.modal.delete(self.displayBales)
        self.modal.delete(self.displayBarricaders)
        self.modal.delete(self.BNImage)
        self.modal.delete(self.BNText)
        self.modal.delete(self.BNbackground)
        self.modal.delete(self.finishButtonWindow)

        # display the final position lists
        self.modal.create_text(
            constants.MODALMIDX, 50, anchor="center", 
            text=("Buggy Navigator: " + 
                (constants.BN.removeprefix("images/")).removesuffix(".png")), 
            font=("Arial", 18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 125, anchor="center", 
            text=("Flaggers: " + 
                self.__produceLines(self.flaggersList, 95)), 
            font=("Arial", 18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 200, anchor="center", 
            text=("Pushers: " + 
                self.__produceLines(self.pushersList, 95)), 
            font=("Arial",18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 275, anchor="center", 
            text=("Barricaders: " + 
                self.__produceLines(self.barricadersList, 95)), 
            font=("Arial", 18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 350, anchor="center", 
            text=("Backups: " + 
                self.__produceLines(self.backupsList,95)), 
            font=("Arial", 18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 425, anchor="center", 
            text=("Video & Timers: " + 
                self.__produceLines(self.videoTimersList, 95)), 
            font=("Arial", 18), fill="White"
        )
        self.modal.create_text(
            constants.MODALMIDX, 500, anchor="center", 
            text=("Bales: " + 
                self.__produceLines(self.balesList, 95)), 
            font=("Arial", 18), fill="White"
        )

        # create the dictionary required by scheduleDocument library
        choicesDict = {
            "flaggers": self.flaggersList, "pushers": self.pushersList, 
            "barricaders": self.barricadersList, "backups": self.backupsList, 
            "bales": self.balesList, "videotimers": self.videoTimersList
        }

        # section to send out email
        self.modal.create_text(957, 25, fill="White", text="Buggy Date:")
        buggyDate = Entry(
            self.window, 
            textvariable=StringVar(self.window, value="DD-MM-YYYY"), bd=0
        )
        self.modal.create_window(1047, 25, width=96, window=buggyDate)
        self.modal.create_text(865, 54, fill="White", text="Email to:")
        emailAddresses = Entry(
            self.window, 
            textvariable=StringVar(self.window, value="user@examaple.com"), bd=0
        )
        self.modal.create_window(995, 54, width=200, window=emailAddresses)
        sendButton = Button(
            self.window, text="Send schedule", 
            highlightbackground=constants.BACKGROUND, bd=0, 
            command=(
                lambda: self.__createAndEmailDocuments(
                    choicesDict, buggyDate.get(), emailAddresses.get()
                )
            )
        )
        self.modal.create_window(1095, 69.5, anchor="ne", window=sendButton)

    def waithere(self, t):
        '''
        Pause our window for [t] millisceonds
        '''
        var = IntVar()
        self.window.after(t, var.set, 1)
        self.window.wait_variable(var)

    def choicesModal(self, pathsChosen, pathsAll, requiredNumbers): 
        '''
        This is the main function for this library. It has the following 
        functionality:
            1. turns the chosen image paths [pathsChosen] into images
            2. turns all image paths [pathsAll] into images
            3. creates a series of animations for displaying which people are 
               selected for which positions
               a. creates a spinning animation looping over all photos
               b. displays a selected member and their position following the
                  spinning animation
               c. updates running lists displayed on the screen mapping selected
                  people to their position
               d. stops by default when all selected members have been assigned
                  their position through the animations
            4. allows you to end the above animations early by the click of a 
               button
            5. displays a final screen containing:
                a. lists of people being mapped to their selected positions
                b. a section to create a schedule based on the selected people
                   and email to a specified email address (assisted by
                   scheduleDocuments custom library)
        Notes:
            1. bases selections for positons off the [requiredNumbers] for each
               postion
            2. assumes [pathsChosen] is randomized
        '''
        # initialize our Buggy Navigator display
        # we can't do this is init for scope of image object
        BNimg = Image.open(constants.BN)
        BNimgTmp = self.__resizeAndCrop(BNimg, constants.BNSIZE)
        self.BNImage = self.modal.create_image(
            1030, 80, anchor = "center", image=BNimgTmp
        )
        self.BNText = self.modal.create_text(
            1030, 134, text="B.N.", font=("Trattatello", 24), 
            fill=constants.GARNET
        )
        BNbbox = self.modal.bbox(self.BNText)
        self.BNbackground = self.modal.create_rectangle(
            BNbbox[0] - 45, BNbbox[1] + 8, BNbbox[2] + 45,  BNbbox[3] - 8, 
            outline="", fill="White"
        )
        self.modal.tag_lower(self.BNbackground, self.BNText)
    
        # give time for the user time to adjust to the screen before animations
        self.waithere(1500)
        
        # creates a list of images for all choices
        imagesChosen = []
        self.modal.images = []
        for path in pathsChosen:
            tmp = Image.open(path)
            img = self.__resizeAndCrop(tmp, constants.PICSIZE)
            imagesChosen.append(img)
            self.modal.images.append(img)

        # creates a list of images for all members (used for animations only)
        imagesAll = []
        self.modal.imagesAll = []
        for path in pathsAll:
            tmp = Image.open(path)
            img = self.__resizeAndCrop(tmp, constants.PICSIZE)
            imagesAll.append(img)
            self.modal.imagesAll.append(img)

        # main play selection animation
        self.__playSelections(
            pathsChosen, imagesChosen, imagesAll, requiredNumbers
        )

        # update our lists to their final forms
        self.__finalizeLists(pathsChosen, requiredNumbers)
        
        # display our last screen after animations are complete
        self.__displayFinal()
