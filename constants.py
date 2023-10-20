
################################################################################ 
########################            CONSTANTS            #######################
################################################################################
'''
    This library defines constants to be used across all files in the app. 
'''

############################ VALUES TO MODIFY PEOPLE ###########################
'''
NOTE: We require that each path provided in these lists leads to an image file
'''
BN = (
    # tweety is the oldest so he will head the program
    "images/Tweety.png" 
)
NEWMEMBERS = [
    # we can leave seniorities empty if we want!
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
NOTE: We require that all names in groups are also in one of the lists of people
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
    # no category: images/Patrick.png (we don't have to group everyone!)
]

####################### VALUES TO MODIFY REQUIRED NUMBERS ######################
'''
NOTE: We require all values to be >= 1
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
