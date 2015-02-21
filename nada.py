import glob, os, sys

ghn = raw_input("Enter a git name: ")

print "Removing extra SoundCues..."

cues = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.SoundCue.data"))

parsed_cues = []

for cuename in cues:
    with open(cuename, "r") as cue:
        newcue = cue.read()
        newcue = newcue[newcue.rfind("Array Sounds = "):]
        newcue = newcue[newcue.rfind("[") + 2:newcue.rfind("]") - 2]
        newcues = newcue.split("\n")
        for cueln in newcues:
            cln = cueln.replace("\t", "")
            if cln == "{":
                continue
            if cln == "},":
                continue
            if cln.startswith("float") == True:
                continue
            cln = cln[cln.rfind(":") + 1:cln.rfind("\"")]
            parsed_cues.append(cln)

sounds = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.wav"))
sounds += glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.mp3"))

for sound in sounds:
    soundname = sound[sound.rfind("\\") + 1:sound.rfind(".")]
    if not soundname in parsed_cues:
        os.remove(sound)
        os.remove(sound + ".meta")

print "Removing extra Archetypes..."
    
levels = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.Level.data"))

parsed_levels = []

for levelname in levels:
    with open(levelname, "r") as level:
        newlevel = level.read()
        newlevels = newlevel.split("\n")
        atp = False
        for levelln in newlevels:
            cln = levelln.replace("\t", "")
            if cln == "Archetyped = ":
                atp = True
            if not atp == False:
                if cln.startswith("string") == True:
                    cln = cln[cln.rfind(":") + 1:cln.rfind("\"")]
                    parsed_levels.append(cln)
                    atp = False

zilches = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.z"))


for zilchname in zilches:
    with open(zilchname, "r") as zilch:
        newzilch = zilch.read()
        newzilches = newzilch.split("\n")
        for zilchln in newzilches:
            cln = zilchln.replace("\t", "")
            if "Archetype.Find(\"" in cln:
                cln = cln[cln.find("Archetype.Find(\"") + len("Archetype.Find(\""):]
                cln = cln[:cln.find("\"")]
                parsed_levels.append(cln)


archetypes = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.Archetype.data"))

for archetype in archetypes:
    archname = archetype[archetype.rfind("\\") + 1:archetype.find(".")]
    if not archname in parsed_levels:
        print archname
        os.remove(archetype)
        os.remove(archetype + ".meta")

print "Removing extra tilemaps..."

tmaps = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*_TileMap[0-9][0-9].*"))

levelnames = []

for level in levels:
    levelnames.append(level[level.rfind("\\") + 1:level.find(".")])

for tmap in tmaps:
    tname = tmap[tmap.rfind("\\") + 1:tmap.find("_")]
    if not tname in levelnames:
        print tname
        os.remove(tmap)
