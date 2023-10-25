# Buggy Randomizer

## Demo

Please view the [full video demo](https://www.youtube.com/watch?v=z_rRfHiElks) (17:34) or [abbreviated video demo](https://www.youtube.com/watch?v=fagQCA8_CvI) (7:00) 
for this project.

## Creator's Note
This project stands as a testament to clarity and effectiveness. The codebase 
highlights my code styling, modularity, documentation, and organization. 
While the underlying logic might not be the most complex challenge I've tackled, 
this goes beyond mere technical details. Rather, it's a reflection of the 
problem solving insights I bring to the table when addressing challenges, as 
well as the practices I perform in doing so. I'm proud to have introduced this 
tool to my fraternity, and it's humbling to have witnessed its success in 
addressing a significant issue. Dive into this README for a deeper understanding 
of the motivations and implementation strategies behind my solution.

## What is Buggy?

### Description
[Buggy](https://www.cmu.edu/buggy) is a unique and longstanding tradition at 
Carnegie Mellon University. It is an interdisciplinary sport that combines the 
talents of designers, engineers, mechanics, and athletes. Participants create a 
"buggy," which is a small, aerodynamic vehicle without an engine, powered solely 
by human effort. In the race, teams of pushers and a driver race around a 
0.84-mile track in Schenley Park's Flagstaff Hill, reaching speeds of up to 40 
mph. This event takes place every April, where students, alumni, and the 
community gather to watch the Buggy teams compete for the annual title.

Buggy events, commonly known as "Rolls," are typically held early on Saturday 
and Sunday mornings at Flagstaff Hill. To ensure the safety of the drivers, hay 
bales, termed "Bales," are strategically placed around the track the night 
before each Roll.

As of 2023, my fraternity ([Pi Kappa Alpha](https://cmupikes.org)) has the most 
first place victories out of any Buggy organization in history, dating back to 
our first win in 1922. 

### Positions
- Drivers: lay down inside of the buggy, navigating it through the track
- Pushers: push the buggies forward, both up and down hills
- Flaggers: hold flags, allowing drivers to navigate specific locations on the 
track
- Video & Timers: capture videos and lap times for analysis
- Bales: set up hay bails alongside edges of the track to keep drivers safe
- Barricaders: maintain hay bails alongside crucial edges of the track to keep
 drivers safe
- Backups (optional): take the place of people in the positions above should a
last minute cancellation occur

## Motivations
The Buggy races occur on major roads around the campus, especially Flagstaff 
Hill, which are essential for daily transportation. To avoid causing significant 
traffic disruptions, these races are scheduled around 5 am, primarily on 
weekends. The corresponding "Bales" setup is usually around 9 or 10 pm the 
previous night. While this early timing can be challenging for participants, 
consistent practice is crucial, especially for pushers and drivers. Hence, 
regular attendance is vital. To streamline this, I introduced a schedule 
randomizer as the first project of the presidency of Pi Kappa Alpha Fraternity 
in 2021. This tool not only removes biases in scheduling but also prevents 
manual scheduling hassles. It was a response to past conflicts within our team. 
The randomizer has since been a successful solution, reducing disputes and 
adding an element of anticipation to the weekly schedule assignments, enhanced
by excited animation embedding within the application.

## Application Overview

## Inputs
- Exemptions: require that `name : string` is NOT added to to the schedule
- Guaranteed: require that `name : string` is added to to the schedule
- Required Numbers:
    1. Pushers: require that `p : int` pushers are added to the schedule
    2. Flaggers: require that `f : int` flaggers are added to the schedule
    3. Video & Timers: require that `vt : int` video & timers are added to the 
    schedule
    4. Bales: require that `bl : int` bales are added to the schedule
    5. Barricaders: require that `br : int` barricaders are added to the 
    schedule
    6. Backups: require that `bk : int` backups are added to the schedule
- Probabilities by Seniority:
    1. New Members: probability `pn : float` of a given new member being 
    selected to the schedule
    2. Freshman: probability `pf : float` of a given freshman being selected to 
    the schedule
    3. Sophomores: `pso : float` of a given sophomore being selected to the 
    schedule
    4. Juniors: `pj : float` of a given junior being selected to the schedule
    5. Seniors: `pse : float` of a given senior being selected to the schedule
- Group Selection: conditional on `g : boolean`, produce a schedule by selecting 
names in groups or individually

### Implementation
- `buggyRandomizer.py`: This file handles all the randomized selection logic. It
encompasses two main types of selection methods:
    1. Normal Selection: individual members are selected at random based on the 
    probabilities provided as inputs.
    2. Group Selection: members are selected in groups, where the probability of 
    a group being selected is the total probability of members being selected 
    individually based on the probabilities provided as inputs.
- `choicesModal.py`: This file provides a series of "spinning" animations that 
map selected names to their respective positions. The animation feature is 
intended to induce excitement surrounding Buggy and the process of generating 
schedules for a given week.
- `scheduleDocuments.py`: This file is to create schedule documents with 
Microsoft Word and send them out to specified email addresses.
- `constants.py`: This file contains key values which remain constant throughout
the execution of the program. This file can be modified in order to update 
*people*, *groups*, *numbers*, or *displays* within the application.
- `images`: This folder contains all image files associated with the program,
particularly those associated with names.
- `past`: This folder contains all Microsoft Word schedule documents generated
by the program for emailing purposes.

## Customization

### Names & Images

Names and images in the application can be modified in two locations: the 
`images` folder and `constants.py` file.
- In `images`, we can remove the image files that are associated with members
we no longer want to include in our app. We can add image files that are 
associated within new members we want to include by adding them as to the 
`images` folder as `{name}.png`, producing the path `images/{name}.png`.
- In `constants.py`, we must remove any members whose image files are not 
included in the `images` folder. We can add any members whose images files
are included in the `images` folder. Specifically, we will want to add them to 
one of the seniorities: `NEWMEMBERS`, `FRESHMAN`, `SOPHOMORE`, `JUNIOR`, 
`SENIOR`. We can also add them to a group under `BUGGYGROUPS`, which should be 
a 2d lists where internal lists represent groups.

### Source Email

This application enables email deliver of schedule documents through the 
`scheduleDocuments.py` library. If you would like to use this feature, you 
must update the environment variables or the logic included within `email` in 
`scheduleDocuments.py`. 
- Update Environment Variables Method: Create a file in the root directory 
titled `.env`. To this file, add `EMAIL={your_email}` and 
`PASSWORD={your_password}` on different lines. Make sure you have 
intalled `python-dotenv` in `requirements.txt` (see below).
- Update Email Logic: Navigate to `scheduleDocuments.py` and findt the `email`
method. Replace any occurances of `os.getenv("EMAIL")` with `{your_email}`, and
any occurances of `os.getenv("PASSWORD")` with `{your_password}`. Note that in
doing this, you should not share you code publicly as you will be exposing 
sensitive information.

## Room for Improvement

### Problem
Every semester, we must update *names*, *seniorities*, *groups*, and the *buggy* 
*navigator*. However, the only way to do so is by manually inserting new images
precisely following the `images/{name}.png` syntax. This can be tedious,
especially with a large number of members.

### Suggestions
Create profiles by name that store information. This way we can automatically 
assign names to seniorities. On top of that create features within the app that
allow you to assign names to different groups and update the Buggy Navigator.

## Installation and Dependencies

Required:
- **Python**: The app can successfully run on `Python 3.9.18`. You will likely 
need `python >=3.9` due to the use of specific methods introduced in 
this version.
- **[python-docx](https://python-docx.readthedocs.io)**: Generate word 
documents.

Optional
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Access 
environment variables from within the program to safely store you email and 
password.

Step-by-step:
1. Clone the repository to your local machine.
2. Navigate to the repository's main directory.
3. Make sure to have `pip` and `Python` installed on your device.
4. Run `pip install -r requirements.txt`.
5. Follow the **Customizaton** section above to adapt the program to fit your 
needs.
6. Run the `buggyRandomizer.py` file using Python.
