
################################################################################ 
########################            CONSTANTS            #######################
################################################################################
'''
    Everything you change between semesters lives here. 
'''

############################ VALUES TO MODIFY PEOPLE ###########################
'''
Every path in these lists must point to an image file.
'''
BN = (
    # Tweety is the oldest, so he heads the program
    "images/Tweety.png" 
)
NEWMEMBERS = [
    # a class year can be empty
]
FRESHMAN = [ # 2004 - present
    "images/Amongus.png", "images/Elsa.png", "images/Chick.png", 
    "images/Elastigirl.png"
]
SOPHOMORES = [ # 2001 - 2003
    "images/Mike.png", "images/Sully.png", "images/Shrek.png", "images/Dory.png"
] 
JUNIORS = [ # 1989 - 2000
    "images/Spongebob.png", "images/Patrick.png", "images/Lisa.png",
]
SENIORS = [ # past - 1988
    "images/Smurfette.png", "images/Grinch.png", "images/Tweety.png",
    "images/Clifford.png"
]

############################ VALUES TO MODIFY GROUPS ###########################
'''
Every name in a group must also be in one of the class year lists above.
'''
BUGGYGROUPS = [
    # red
    ["images/Elastigirl.png", "images/Clifford.png", "images/Amongus.png"],
    # blue
    ["images/Smurfette.png", "images/Elsa.png", "images/Sully.png", 
    "images/Dory.png"],
    # yellow 
    ["images/Tweety.png", "images/Lisa.png", "images/Spongebob.png"],
    # green
    ["images/Chick.png", "images/Shrek.png", "images/Mike.png", 
    "images/Grinch.png"] 
    # not everyone needs a group: images/Patrick.png has none
]

####################### VALUES TO MODIFY REQUIRED NUMBERS ######################
'''
Every value must be at least 1.
'''
PUSHERGROUPS = 4
NUMPUSHERS = 15
NUMFLAGGERS = 10
NUMBALES = 20
NUMBACKUPS = 10
NUMVIDEOTIMERS = 5
NUMBARRICADERS = 10

########################### VALUES TO MODIFY SCHEDULE ##########################
GENERALSCHEDULE = """
    5:35 AM        Drops Open
    5:50 AM        Barricader's Meeting
    6:00 AM        Roads Close
    6:35 AM        Drops Close
    6:40 AM        Flaggers Meeting
    6:45 AM        Chairmen's Meeting
    6:50 AM        Drive Around
    6:55 AM        First Possible Rolls
    7:05 AM        Sunrise 
    9:00 AM        Last Rolls
    """

########################### VALUES TO MODIFY DISPLAY ###########################
WIDTH = 1250
HEIGHT = 750
MIDX = WIDTH / 2
MIDY = HEIGHT / 2
MODALMIDX = 550
PICSIZE = 290
BNSIZE = 135
GARNET = "#7A222E"
GOLD =  "Gold3"
BACKGROUND = "black"
