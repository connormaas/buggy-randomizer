# Buggy Randomizer

Fair, randomized scheduling for CMU Buggy practice, with an animated reveal, Word schedules, and email delivery.

**Demo:** [watch on YouTube](https://www.youtube.com/watch?v=hKgC_VTFzzU) (7 min)

## Background

[Buggy](https://www.cmu.edu/buggy) is a Carnegie Mellon race that dates back to 1920. Teams build engineless vehicles, and a driver lies inside while a relay of pushers runs it up the hills of a 0.84 mile course through Schenley Park, hitting up to 40 mph on the downhill. My fraternity, [Pi Kappa Alpha](https://cmupikes.org), has won more races than any other organization, starting in 1922.

Practices ("Rolls") run on real roads, so they start around 5 AM on weekends, and the night before, teams line the course with hay bales ("Bales"). Every week we need people for each role:

- **Pushers:** push the buggy up the hills
- **Flaggers:** guide drivers through key turns
- **Video & Timers:** record runs and lap times
- **Bales:** set up the hay bales
- **Barricaders:** hold the bales in place along key edges
- **Backups:** fill in for last minute cancellations

## Why I Built It

Picking people for 5 AM shifts by hand was slow and caused arguments. As president in 2021, I built this to make it fair and automatic: it picks the schedule, reveals it with a spinning animation, and emails out the documents. The arguments stopped.

## How It Works

**Inputs**
- **Exemptions** and **guaranteed** names
- **Headcount** for each role
- **Probability by class year**, from new members to seniors
- **Group selection**, which picks whole groups instead of individuals

**Files**
- `buggyRandomizer.py`: the app and selection logic. In group mode, a group's chance is the sum of its members' chances.
- `choicesModal.py`: the spinning reveal
- `scheduleDocuments.py`: builds the Word schedules and emails them
- `constants.py`: members, groups, headcounts, and display settings
- `images/`: a photo per member
- `past/`: generated schedules

## Setup

Requires Python 3.9+.

```bash
git clone https://github.com/connormaas/buggy-randomizer.git
cd buggy-randomizer
pip install -r requirements.txt
python buggyRandomizer.py
```

**Members:** add a photo at `images/{name}.png`, then add the name to its class year in `constants.py` (`NEWMEMBERS`, `FRESHMAN`, `SOPHOMORES`, `JUNIORS`, `SENIORS`) and optionally to a group in `BUGGYGROUPS`.

**Email:** add a `.env` file in the repo root. It's git ignored, so credentials stay out of the code.

```
EMAIL=your_email
PASSWORD=your_password
```

## Next Up

Member profiles with in app editing, so the roster doesn't need manual updates every semester.
