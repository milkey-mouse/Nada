import glob, os, sys, csv, msvcrt
from tempita import looper
ghn = "TheLegendofAdlez"

levels = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.Level.data"))

archetypes = []

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
                    archetypes.append(cln)
                    atp = False

archetypefiles = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.Archetype.data"))

zilches = []

for archetype in archetypefiles:
    scripts = []
    archname = archetype[archetype.rfind("\\") + 1:archetype.find(".")]
    with open(archetype, "r") as afile:
        if archname in archetypes:
            for line in afile.read().split("\n"):
                if line.startswith("	") and line.endswith(" = "):
                    fz = line.replace(" = ", "").replace("	", "")
                    if fz not in zilches:
                        zilches.append(fz)

core_remove_z = ["Named", "Archetyped", "Cog"]
game_remove_z = ["EnemyTag"] #not core zilches

game_remove_z += core_remove_z

for zilch in game_remove_z:
    zilches.remove(zilch)

accepted_types = ["Boolean", "Real", "Integer", "String"]

zilch_vars = {}

for zilch in zilches:
    zname = os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\\" + zilch + ".z")
    if not os.path.isfile(zname):
        zilches.remove(zilch)
        continue
    with open(zname, "r") as zilchfile:
        _zvars = []
        for line in zilchfile.read().split("\n"):
            if "var" in line:
                nl = line.strip()
                nl = nl[4:]
                if nl[0].isupper():
                    nlt = nl[nl.find(":") + 2:nl.rfind(" =")]
                    nl = nl[:nl.find(":") - 1]
                    if nlt in accepted_types:
                        _zvars.append((zilch, nl, nlt))
        zilch_vars[zilch] =_zvars

arch_vars = {}

for archetype in archetypefiles:
    scripts = []
    archname = archetype[archetype.rfind("\\") + 1:archetype.find(".")]
    _avars = []
    with open(archetype, "r") as afile:
        if archname in archetypes:
            for line in afile.read().split("\n"):
                if line.startswith("	") and line.endswith(" = "):
                    fz = line.replace(" = ", "").replace("	", "")
                    if fz in zilch_vars:
                        _avars.append(zilch_vars[fz])
    arch_vars[archname] = _avars

import pprint
pp = pprint.PrettyPrinter(indent=4)
ppo = pp.pformat(arch_vars)
#print ppo
with open("out.txt", "w") as outfile:
    outfile.write(ppo)
#os.startfile("out.txt")


with open('avoid.csv', 'w') as csvfile:
    avoids = csv.writer(csvfile)
    for arch in arch_vars:
        viq = arch_vars[arch]
        for script in viq:
            for var in script:
                siq = var[0] + "." + var[1]
                print siq + " "
                ans = msvcrt.getch().upper()
                if ans == "C":
                    avoids.writerow((var[0], var[1], var[2]))