import decimal
decimal.getcontext().prec = 6

objects = [ # index 1 is force of the object hanging, 2 is the distance from the string holding it from above in centimeters.
    [decimal.Decimal(0.0981),decimal.Decimal(17.8)],
    [decimal.Decimal(0.0339),decimal.Decimal(10.6)],
    [decimal.Decimal(0.0678),decimal.Decimal(16.2)],
    [decimal.Decimal(0.0336),decimal.Decimal(17.2)],
    [decimal.Decimal(0.0322),decimal.Decimal(18)],
    [decimal.Decimal(0.0387),decimal.Decimal(8.8)],
    [decimal.Decimal(0.0313),decimal.Decimal(20)],
    [decimal.Decimal(0.0358),decimal.Decimal(17)],
    [decimal.Decimal(0.024),decimal.Decimal(12.8)],
    [decimal.Decimal(0.0194),decimal.Decimal(14.4)]
]

levels = { # Level 1 is the top of the mobile and it decreases. Dropstring is the distance from the hanging point to the string that drops down to the next level.
    "level6": {"left": [objects[8]], "right": [objects[9]], "dropstring": False},
    "level5": {"left": [True], "right": [objects[7]], "dropstring": decimal.Decimal(9.5)},
    "level4": {"left": [objects[6]], "right": [True], "dropstring": decimal.Decimal(6)},
    "level3": {"left": [objects[4]], "right": [True, objects[5]], "dropstring": decimal.Decimal(2.5)},
    "level2": {"left": [objects[3], objects[2]], "right": [True, objects[1]], "dropstring": decimal.Decimal(4.6)},
    "level1": {"left": [objects[0]], "right": [True], "dropstring": decimal.Decimal(4.1)}
}


sticks = [ # forces of each stick, bottom to top of the mobile
    decimal.Decimal(0.0282),
    decimal.Decimal(0.0301),
    decimal.Decimal(0.0315),
    decimal.Decimal(0.0264),
    decimal.Decimal(0.0281),
    decimal.Decimal(0.0269)
]


string = decimal.Decimal(0.00157) # calculated newton force of each segment of string approximately
level_prompt = int(input("Level: "))
target_level = levels[f"level{level_prompt}"]


def getSticks():
    # Sticks
    force_total = 0
    numSticks = 6-level_prompt
    sticksTargetIndex = numSticks-1
    for i in range(len(sticks)):
        if i>sticksTargetIndex:
            break
        force_total = force_total+sticks[i]
    
    print(f"Sticks force: {force_total}")
    return force_total

def getStrings(): # DOESNT COUNT FIRST DROP-DOWN STRING
    force_total = decimal.Decimal(0)
    strings = (6-level_prompt)-1
    objectStrings = 0
    targetIndex = strings
    for i in range(len(levels)):
        if i>targetIndex:
            break
        for s in levels[f"level{6-i}"]["left"]:
            if s != True:
                objectStrings=objectStrings+1
                force_total=force_total+s[0]
        for s in levels[f"level{6-i}"]["right"]:
            if s != True:
                objectStrings=objectStrings+1
                force_total=force_total+s[0]
                
    strings=strings+objectStrings
    force_total = force_total+(strings * string)
    print(f"Object strings: {objectStrings}")
    print(f"Total strings: {strings}")
    print(f"Strings/Objects force: {force_total}")
    return force_total


force_strings = getStrings()
force_sticks = getSticks()
force_left = decimal.Decimal(0)
force_right = decimal.Decimal(0)
torque_left = decimal.Decimal(0)
torque_right = decimal.Decimal(0)


# OBJECTS ON TARGET LEVEL ARE EXCLUDED FROM FORCE TOTAL VARS
for s in target_level["left"]:
    if s != True:
        torque_left = torque_left+(s[1]*(s[0]+string))
    if s == True:
        force_left=force_left+string
        force_left=force_left+force_sticks
        force_left=force_left+force_strings
        if level_prompt < 6:
            torque_left = torque_left+(target_level["dropstring"] * force_left)
for s in target_level["right"]:
    if s != True:
        torque_right = torque_right+(s[1]*(s[0]+string))
    if s == True:
        force_right=force_right+string
        force_right=force_right+force_sticks
        force_right=force_right+force_strings
        if level_prompt < 6:
            torque_right = torque_right+(target_level["dropstring"] * force_right)


print(f"Force left: {force_left}")
print(f"Force right: {force_right}")
print(f"Torque left: {torque_left}")
print(f"Torque right: {torque_right}")
print(f"Percent Difference: {(abs(torque_left-torque_right)/((torque_left+torque_right)/2))*100}")