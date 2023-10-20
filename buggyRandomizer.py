################################################################################ 
#####################                                     ###################### 
########################      BUGGY RANDOMIZER       ########################### 
#############################                   ################################ 
################################################################################ 
# Connor Maas
################################################################################ 
'''
This is the main file for the application, containing window initializaiton and 
randomization logic. It leverages custom libraries to showcase selections via 
animations and facilitates the generation and emailing of schedule documents
'''
import os
import signal
import random
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from choicesModal import ChoicesModal
import constants

###################################   APP   ####################################
class App:
    def __init__(self, window):
        # Initialize groups toggle
        self.groupsOn = True

        # create canvas and some inital variables
        self.window = window
        self.canvas = Canvas(
            window, width=constants.WIDTH, height=constants.HEIGHT, 
            bg=constants.BACKGROUND, bd=0, highlightthickness=0
        )
        self.canvas.pack(fill="both",expand=True)

        # header section
        Timg1 = Image.open("images/Pike.png")
        (Twidth, Theight) = Timg1.size
        Timg2 = ImageTk.PhotoImage(
            Timg1.resize((int(Twidth * 0.45), int(Theight * 0.45)), 
            Image.LANCZOS)
        )
        self.canvas.image = Timg2
        self.canvas.create_image(
            constants.MIDX, 75, anchor="center", image=Timg2
        )
        self.canvas.create_text(
            constants.MIDX - 2, 79, text="BUGGY RANDOMIZER", 
            font=("Helvetica Bold", 75), fill="gold4"
        )  
        self.canvas.create_text(
            constants.MIDX, 81, text="BUGGY RANDOMIZER", 
            font=("Helvetica Bold", 75), 
            fill=constants.GOLD
        )    
        restartButton = Button(
            window, text="Restart", command=self.restart, 
            highlightbackground=constants.BACKGROUND
        )
        self.canvas.create_window(10, 5, anchor="nw", window=restartButton)
        
        # exemptions section
        self.canvas.create_text(
            constants.MIDX, constants.MIDY - 215, text="Exemptions", 
            fill="White", font=("Arial Bold", 25)
        )
        BNname = constants.BN.removeprefix("images/").removesuffix(".png")
        self.exemptionsEntry = self.createEntryHelper(
            constants.MIDX, constants.MIDY - 185, BNname
        )

        # guaranteed section
        self.canvas.create_text(
            constants.MIDX, constants.MIDY - 140, text="Guaranteed", 
            fill="White", font=("Arial Bold", 25)
        )
        self.guaranteedEntry = self.createEntryHelper(
            constants.MIDX, constants.MIDY - 110, ""
        )

        # position sliders section
        self.pushersSlider = self.createPositionSlider(
            constants.MIDX - 350, constants.MIDY - 25, "Pushers Required", 
            constants.NUMPUSHERS
        )
        self.flaggersSlider = self.createPositionSlider(
            constants.MIDX - 350, constants.MIDY + 75, "Flaggers Required", 
            constants.NUMFLAGGERS
        )
        self.videoTimersSlider = self.createPositionSlider(
            constants.MIDX - 350, constants.MIDY + 175, 
            "Video & Timers Required", constants.NUMVIDEOTIMERS
        )
        self.balesSlider = self.createPositionSlider(
            constants.MIDX + 50, constants.MIDY - 25, "Bales Required", 
            constants.NUMBALES
        )
        self.barricadersSlider = self.createPositionSlider(
            constants.MIDX + 50, constants.MIDY + 75, "Barricaders Required", 
            constants.NUMBARRICADERS
        )
        self.backupsSlider = self.createPositionSlider(
            constants.MIDX + 50, constants.MIDY + 175, "Backups Required", 
            constants.NUMBACKUPS
        )

        # probability entries section
        self.newmemberProb = self.createEntryHelper(
            constants.MIDX + 400, constants.MIDY - 30, 1, width=250
        )
        self.freshmanProb = self.createEntryHelper(
            constants.MIDX + 400, constants.MIDY + 25, 1, width=250
        )
        self.sophomoreProb = self.createEntryHelper(
            constants.MIDX + 400, constants.MIDY + 80, 1, width=250
        )
        self.juniorProb = self.createEntryHelper(
            constants.MIDX + 400, constants.MIDY + 135, 1, width=250
        )
        self.seniorProb = self.createEntryHelper(
            constants.MIDX + 400, constants.MIDY + 190, 1, width=250
        )
        self.canvas.create_text(
            constants.MIDX + 400, constants.MIDY - 55, 
            text="New Member Probability", fill="White", font=("Arial", 15)
        )
        self.canvas.create_text(
            constants.MIDX + 400, constants.MIDY, text="Freshman Probability", 
            fill="White", font=("Arial", 15)
        )
        self.canvas.create_text(
            constants.MIDX + 400, constants.MIDY + 55, 
            text="Sophomore Probability", fill="White", font=("Arial", 15)
        )
        self.canvas.create_text(
            constants.MIDX + 400, constants.MIDY + 110, 
            text="Junior Probability", fill="White", font=("Arial", 15)
        )
        self.canvas.create_text(
            constants.MIDX + 400, constants.MIDY + 165, 
            text="Senior Probability", fill="White", font=("Arial", 15)
        )

        # main randomize button and select by groups toggle
        self.canvas.create_text(
            constants.WIDTH / 2, constants.HEIGHT - 150, fill="White", 
            text="Select By Groups"
        ) 
        groupsButton = Button(
            window, text="On", highlightbackground=constants.BACKGROUND, 
            width=10, bd=2, command=self.groupsFlipper
        )
        self.groupsButtonWindow = self.canvas.create_window(
            constants.WIDTH / 2, constants.HEIGHT - 125, anchor="center", 
            window=groupsButton
        )
        self.runButton = Button(
            window, text="  GENERATE RANDOM SCHEDULE  ", fg=constants.GARNET, 
            bd=0, highlightbackground=constants.GOLD, font=("Trattatello", 26), 
            command=self.executeRandomizationProgram
        )
        self.runButtonWindow = self.canvas.create_window(
            constants.WIDTH / 2, constants.HEIGHT - 65, window=self.runButton
        )  

    def createEntryHelper(self, x, y, value, width=750):
        '''
        Helper for creating entries, shortening repetiion in initialization
        '''
        entry = Entry(
            self.window, textvariable=StringVar(self.window, value=value), bd=0
        )
        self.canvas.create_window(x, y, width=width, window=entry)
        return entry

    def createPositionSlider(self, x, y, text, to, tickinterval=1, width=350):
        '''
        Helper for creating position sliders, shortening repetiion in 
        initialization
        '''
        slider = Scale(
            self.window, fg="White", from_=0, to=to, bg=constants.BACKGROUND, 
            bd=-2.5, tickinterval=tickinterval, orient=HORIZONTAL
        )
        self.canvas.create_window(x, y, width=width, window=slider)
        self.canvas.create_text(
            x, y - 30, text=text, fill="White", font=("Arial", 15)
        )
        return slider

    def groupsFlipper(self):
        '''
        Function to toggle the select by groups button
        '''
        if self.groupsOn:
            groupsButton = Button(
                self.window, text="Off", bd=2, width=10, 
                highlightbackground=constants.BACKGROUND, 
                command=self.groupsFlipper
            )
            self.canvas.create_window(
                constants.WIDTH/2, constants.HEIGHT - 125, anchor="center", 
                window=groupsButton
            )
        else:
            groupsButton = Button(
                self.window, text="On", bd=2, width=10, 
                highlightbackground=constants.BACKGROUND, 
                command=self.groupsFlipper
            )
            self.canvas.create_window(
                constants.WIDTH / 2, constants.HEIGHT - 125, anchor="center", 
                window=groupsButton
            )
        self.groupsOn = not self.groupsOn

    def flatten(self, L):
        '''
        General function which flattens a 2D list
        '''
        flattened = []
        for sublist in L:
            for item in sublist:
                flattened.append(item)
        return flattened
    
    def restart(self):
        '''
        Function to re-run the app
        '''
        if messagebox.askokcancel(
            "Restart", "Are you sure you want to restart the application?"
        ):
            self.window.destroy()
            main()

    def validateProbs(self):
        '''
        Checks the validity of probability entries
        '''
        if not isinstance(self.newmemberProb.get(), int):
            try:
                int(self.newmemberProb.get())
                int(self.freshmanProb.get())
                int(self.sophomoreProb.get())
                int(self.juniorProb.get())
                int(self.seniorProb.get())
            except ValueError:
                try: 
                    float(self.newmemberProb.get())
                    float(self.freshmanProb.get())
                    float(self.sophomoreProb.get())
                    float(self.juniorProb.get())
                    float(self.seniorProb.get())
                except ValueError:
                    messagebox.showerror(
                        "Error", "Please enter a number for all probabilities"
                    ) 
                    return False
        return True

    def parseEntry(self, type):
        '''
        Depending on [type], this funciton validates the entry of exemptions or 
        guaranteed. Validation occurs by checking if the provided names matches
        a name in constants.py (i.e. - if a provided name is "John", it will 
        check if "images/John.png" exists in constants)

        Notes: this functionality should be improved because right now provided
        names must match .png file names in the images folder and are case 
        sensitive (this is hard on this user)
        '''
        if type == "exemptions":
            names = self.exemptionsEntry.get()
        else:
            names = self.guaranteedEntry.get()
        
        # align input names with path names by adding file name decoration
        names = names.split(",")
        if len(names) == 0 or names[0] == "":
            return ([], True)
        result = []
        for names in names:
            result.append("images/" + names.strip() + ".png")
        
        # check if each decorated name exists in constants.py creating an error 
        # popup if not
        paths = [
            constants.NEWMEMBERS, 
            constants.FRESHMAN, 
            constants.SOPHOMORES, 
            constants.JUNIORS, 
            constants.SENIORS
        ]
        paths = self.flatten(paths)
        for path in result:
            if path not in paths:
                almostName = path.removesuffix(".png")
                name = almostName.removeprefix("images/")
                messagebox.showerror(
                    "Error", f'"{name}" is not a known name. Check ' +  
                    'constants.py for a list of names (ex: if ' + 
                    '"images/John.png" is in constants.py, then "John" is a ' +
                    'known name).'
                )
                return ([], False)
        
        return (result, True)

    def nestedMap(self, nestedL, valuesList):
        '''
        Takes a nested list [nestedL] and a list [valuesList] such that 
        len(nestL) == len(valueList). Returns a 1D list [res] where
        len(res) == len(flatten(nestedL)) and each values in res aligns with
        M[i] for each i in nestedL
        '''
        res = []
        i = 0
        for L in nestedL:
            for _ in L:
                res.append(valuesList[i])
            i += 1
        return res

    def createProbMapping(self):
        '''
        Uses the the current probability entries and to generate mapping between 
        members and their probabilites of being selected. It returns two lists:
            1. a list of members
            2. a list of probabilities where probabilities[i] is the probability
               of member of [i] being selected
        It also checks that the probabilites at least one probability is greater
        than zero and returns None if this is not the case
        '''
        pplBySeniority = []
        probBySeniority = []
        if float(self.newmemberProb.get()) > 0:
            pplBySeniority.append(constants.NEWMEMBERS.copy())
            probBySeniority.append(float(self.newmemberProb.get()))
        if float(self.freshmanProb.get()) > 0:
            pplBySeniority.append(constants.FRESHMAN.copy())
            probBySeniority.append(float(self.freshmanProb.get()))
        if float(self.sophomoreProb.get()) > 0:
            pplBySeniority.append(constants.SOPHOMORES.copy())
            probBySeniority.append(float(self.sophomoreProb.get()))
        if float(self.juniorProb.get()) > 0:
            pplBySeniority.append(constants.JUNIORS.copy())
            probBySeniority.append(float(self.juniorProb.get()))
        if float(self.seniorProb.get()) > 0:
            pplBySeniority.append(constants.SENIORS.copy())
            probBySeniority.append(float(self.seniorProb.get()))
        
        # nobody could be selected because all probabilites set to zero
        if len(pplBySeniority) == 0:
            messagebox.showerror(
                "Error", "At least one probability must be greater than zero"
            )
            return None
        
        probs = self.nestedMap(pplBySeniority, probBySeniority)
        return (self.flatten(pplBySeniority), probs)

    def removeExceptions(
            self, people, probs, exemptions, guaranteed, buggyGroups
        ):
        '''
        This function destructively modifies the lists [people], [probs], and 
        [buggyGroups] based on the lists [exemptions] and [guaranteed]. 
        Specifically, all members included in exemptions or guaranteed will be 
        removed from buggyGroups and people, along with their corresponding 
        probability of being selected contained in probs
        '''
        cumIdx = 0
        for path in (exemptions + guaranteed):
            if path in people:
                probs.pop(people.index(path))
                people.remove(path)
            else:
                cumIdx += 1
            for group in buggyGroups:
                if path in group:
                    group.remove(path)

    def getRequiredPositionCount(self, people, guaranteed):
        '''
        This function finds the total required positon count based on the 
        current slider values for each position. It also provides a error
        pop up when the requiredPositionTotal > available where available
        == len(people) + len(guaranteeed)

        Note: it assumes that guaranteed and people do not overlap and include
        everyone who is not exempt
        '''
        requiredPositionCount = (
            self.flaggersSlider.get() + self.pushersSlider.get() + 
            self.barricadersSlider.get() + self.backupsSlider.get() + 
            self.balesSlider.get() + self.videoTimersSlider.get()
        )
        
        if requiredPositionCount < 1: 
            messagebox.showerror(
                "Error", "Choose at least one position to fill"
            )
            return None     

        if len(people) + len(guaranteed) < requiredPositionCount:
            if len(people) + len(guaranteed) == 0:
                messagebox.showerror(
                    "Error", "There are no possible candidates for the " + 
                    f"required {requiredPositionCount} positions. Update " + 
                    "probabilites or exemptions to increase the number of " + 
                    "candidates."
                )
            elif len(people) + len(guaranteed) == 1:
                messagebox.showerror("Error", "There is only {len(people)} " + 
                    "possible candidate for the required " + 
                    f"{requiredPositionCount} positions. Update probabilites " + 
                    "or exemptions to increase the number of candidates."
                )
            else:
                messagebox.showerror("Error", f"There are only {len(people)} " +
                    "possible candidates for the required " + 
                    f"{requiredPositionCount} positions. Update probabilites " + 
                    "or exemptions to increase the number of candidates."
                )
            return None
        
        return requiredPositionCount

    def select(self, people, probs, count, guaranteed):
        '''
        Along with other paremeters, this fucntion takes in a list of [people] 
        and a list of [probs] mapping people[i] to a respective probability in 
        probability[i]. It returns a list in random order that is composed of 
        [guaranteed] and a random selection of [people] of length [count] based 
        on probabilities provided in [probs]

        Note: we require that len([people]) >= [count]
        '''
        selections = random.choices(people, weights=probs, k=count)
        return random.sample(
            selections + guaranteed, len(selections + guaranteed)
        )


    def selectByGroups(self, people, probs, count, guaranteed, buggyGroups):
        '''
        Along with other paremeters, this fucntion takes in a list of [people] 
        and a list of [probs] mapping people[i] to a respective probability in 
        probability[i]. It also takes in [buggyGroups], which is a 2D list 
        grouping together members in [people] using internal lists. This 
        function returns a list in random order that is composed of [guaranteed] 
        and a selection of [people] of length [count] based on the following 
        randomized process:
            1. each group is assigned a probability which is the sum of the 
               probabilities of each of it's members being selected
            2. if a person is not assigned to a group, they are given their own
               solo group where the probability of that group being selected
               is just the probability of them being selected overall
            3. groups are selected at random and added to the resulting 
               selctions until the size of the resulting selections meets the
               [count] requirement
            4. if a group being added to the selection would cause the selection
               set to be larger than [count], we only add part of that group by
               randomly selecting it's members based on their respective 
               probabilities

        Note: we require that len([people]) >= [count]
        '''
        buggyGroups = buggyGroups.copy()
        # update buggy groups to contain all members (that is, if a member is
        # not specified in a group then add them to their own solo group)
        additionalGroups = []
        for person in people:
            found = False
            for group in buggyGroups:
                if person in group:
                    found = True
            if not found:
                additionalGroups.append([person])
        buggyGroups += additionalGroups

        # clean up groups to make sure none are empty
        for group in buggyGroups:
            if len(group) == 0:
                buggyGroups.remove(group)

        # create probability mapping for group selection (sum of probs of group 
        # members)
        groupProbs = []
        for group in buggyGroups:
            totalProb = 0
            for person in group:
                totalProb += probs[people.index(person)]
            groupProbs.append(totalProb)

        # select groups randomly by total probabililty one at a time and add
        # members within those groups 
        selections = []
        while count > 0:
            group = (random.choices(buggyGroups, weights=groupProbs, k=1))[0]
            amountToSelect = min(count, len(group))

            if amountToSelect == len(group):
                selections += group
            else:
                probsByPerson = []
                for person in group:
                    probsByPerson.append(probs[people.index(person)])
                selections += self.select(
                    group, probsByPerson, amountToSelect, []
                )

            count -= amountToSelect
            groupProbs.pop(buggyGroups.index(group))
            buggyGroups.remove(group)
        
        # add guaranteed to our selection
        return random.sample(
            selections + guaranteed, len(selections + guaranteed)
        )

    def executeRandomizationProgram(self):
        '''
        This function is associated with the "generate random schedule" button
        and encompasses the main logic of this application. It has the following 
        behavior:
            1. validates all 14 inputs (exemptions/guaranteed, required position 
               counts, probabilities, group selection) with robust error 
               handling, ensuring a user cannot break the program
            2. generates a random selection of members, mapping them to specific
               positions based on the provided inputs (see [README.md] or the 
               [selectByGroups] and [select] functions in this file for more 
               details on behavior)
            3. uses a custom library, [choicesModal], which displays choices 
               through animations
            4. [choicesModal] also allows the user to compile the schedule into 
               a word document and email it to specified addresses using the 
               custom library, [scheduleDocument]
        '''
        # validation on inputs
        if not self.validateProbs():
            return None
        (guaranteed, validGuaranteed) = self.parseEntry("guaranteed")
        (exemptions, validExemptions) = self.parseEntry("exemptions")
        if not validGuaranteed or not validExemptions:
            return None
        for person in guaranteed:
            if person in exemptions:
                person = person.removeprefix("images/")
                person = person.removesuffix(".png")
                messagebox.showerror(
                    "Error", f"{person} cannot be exempt and guaranteed"
                )
                return None

        # map probabilities to people based on inputs
        res = self.createProbMapping()
        if not res:
            return None
        (people, probs) = res

        # remove the exempted or guaranteeed so we can handle seperately
        # this funciton is desctructive so we must copy buggy groups constant
        buggyGroups = constants.BUGGYGROUPS.copy()
        self.removeExceptions(
            people, probs, exemptions, guaranteed, buggyGroups
        )
    
        # get required count based on inputs with error checking 
        requiredPositionCount = (
            self.getRequiredPositionCount(people, guaranteed)
        )
        if not requiredPositionCount:
            return None

        # make selections
        if self.groupsOn:
            choices = self.selectByGroups(
                people, probs, requiredPositionCount - len(guaranteed), 
                guaranteed, buggyGroups
            )
        else:
            choices = self.select(
                people, probs, requiredPositionCount - len(guaranteed), 
                guaranteed
            )
        
        # display selections using custom ChoicesModal library
        requiredPositions = {
            "flaggers": self.flaggersSlider.get(), 
            "pushers": self.pushersSlider.get(), 
            "barricaders": self.barricadersSlider.get(), 
            "backups": self.backupsSlider.get(), 
            "bales": self.balesSlider.get(), 
            "videotimers":  self.videoTimersSlider.get()
        }
        self.canvas.delete(self.runButtonWindow)
        choicesModal = ChoicesModal(self.window)
        choicesModal.choicesModal(choices, people, requiredPositions)

###################################   MAIN   ################################### 
def quitAll(window):
    '''
    Function to exit the window and terminate the app safely without causing
    errors or interfering with other programs

    Notes: can be executed at any point during this app's execution
    '''
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        try:
            window.destroy()
            os.kill(os.getpid(), signal.SIGTERM)
        except Exception as e:
            os._exit(1)

def initializeWindow():
        '''
        Initialize our window with the following properties:
            1. Locked width and height
            2. Initially positioned in top center of screen
        '''
        window = Tk()
        window.title("Buggy Randomizer")
        window.configure(width=constants.WIDTH, height=constants.HEIGHT)
        window.resizable(width=False, height=False)
        window.configure(bg=constants.BACKGROUND)  
        window.protocol("WM_DELETE_WINDOW", lambda: quitAll(window))
        winWidth = window.winfo_reqwidth()
        posRight = int(window.winfo_screenwidth() / 2 - winWidth / 2)
        window.geometry("+{}+{}".format(posRight, 0))
        return window

def main():
    window = initializeWindow()
    App(window)
    window.mainloop()

if __name__ == '__main__':
  main()
