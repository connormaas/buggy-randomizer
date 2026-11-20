################################################################################ 
#####################                                     ###################### 
########################      BUGGY RANDOMIZER       ########################### 
#############################                   ################################ 
################################################################################ 
# Connor Maas
################################################################################ 
'''
The app's entry point: sets up the window and runs the randomization. The
animations and the schedule documents live in their own modules.
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

        # canvas and starting values
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
        Creates an entry field
        '''
        entry = Entry(
            self.window, textvariable=StringVar(self.window, value=value), bd=0
        )
        self.canvas.create_window(x, y, width=width, window=entry)
        return entry

    def createPositionSlider(self, x, y, text, to, tickinterval=1, width=350):
        '''
        Creates a position slider
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
        Toggles group selection on and off
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
        Flattens a 2D list
        '''
        flattened = []
        for sublist in L:
            for item in sublist:
                flattened.append(item)
        return flattened
    
    def restart(self):
        '''
        Restarts the app
        '''
        if messagebox.askokcancel(
            "Restart", "Are you sure you want to restart the application?"
        ):
            self.window.destroy()
            main()

    def validateProbs(self):
        '''
        Checks that every probability entry is a valid number
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
        Validates the exemptions or guaranteed entry, depending on [type]. Each
        name must match a member in constants.py, so "John" is valid when
        "images/John.png" is listed there.

        Names are case sensitive and must match the image file names exactly.
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
        Maps each member to their chance of being picked, using the current
        probability entries. Returns two lists:
            1. the members
            2. their probabilities, where probabilities[i] belongs to members[i]
        Returns None if every probability is zero.
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
        
        # every probability is zero, so nobody can be picked
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
        Removes everyone in [exemptions] and [guaranteed] from [people],
        [probs], and [buggyGroups]. Mutates all three in place.
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
        Adds up the number of people the sliders ask for. Shows an error if
        that's more than everyone available, len(people) + len(guaranteed).

        Assumes guaranteed and people don't overlap and together cover everyone
        who isn't exempt.
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
                    "probabilities or exemptions to increase the number of " + 
                    "candidates."
                )
            elif len(people) + len(guaranteed) == 1:
                messagebox.showerror("Error", "There is only {len(people)} " + 
                    "possible candidate for the required " + 
                    f"{requiredPositionCount} positions. Update probabilities " + 
                    "or exemptions to increase the number of candidates."
                )
            else:
                messagebox.showerror("Error", f"There are only {len(people)} " +
                    "possible candidates for the required " + 
                    f"{requiredPositionCount} positions. Update probabilities " + 
                    "or exemptions to increase the number of candidates."
                )
            return None
        
        return requiredPositionCount

    def select(self, people, probs, count, guaranteed):
        '''
        Picks [count] of [people] at random, weighted by [probs] (probs[i] is
        people[i]'s chance), adds [guaranteed], and returns everyone shuffled.

        Requires len(people) >= count.
        '''
        selections = random.choices(people, weights=probs, k=count)
        return random.sample(
            selections + guaranteed, len(selections + guaranteed)
        )


    def selectByGroups(self, people, probs, count, guaranteed, buggyGroups):
        '''
        Like select, but picks whole groups from [buggyGroups] (a list of
        lists of members) instead of one person at a time:
            1. a group's chance is the sum of its members' chances
            2. anyone without a group gets a group of their own
            3. groups are picked at random until there are [count] people
            4. if the last group would go over [count], only some of its
               members are picked, weighted by their chances
        Returns the picks plus [guaranteed], shuffled.

        Requires len(people) >= count.
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

        # pick groups one at a time, weighted by total probability, and add
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
        Runs when "generate random schedule" is pressed:
            1. validates all 14 inputs (exemptions, guaranteed, position counts,
               probabilities, and group selection), with an error for anything
               invalid
            2. picks members and assigns them to positions (see [select] and
               [selectByGroups])
            3. reveals the picks with the [choicesModal] animation
            4. from there, the schedule can be saved as a Word document and
               emailed out with [scheduleDocuments]
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

        # pull out the exempt and guaranteed members so they're handled separately
        # removeExceptions mutates its inputs, so work on a copy of the groups
        buggyGroups = constants.BUGGYGROUPS.copy()
        self.removeExceptions(
            people, probs, exemptions, guaranteed, buggyGroups
        )
    
        # total people needed, with error checking
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
        
        # reveal the picks with the ChoicesModal animation
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
    Closes the window and exits cleanly. Safe to call at any point.
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
