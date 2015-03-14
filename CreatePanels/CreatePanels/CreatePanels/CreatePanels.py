import glob, os, sys, csv, msvcrt
import pprint
from jinja2 import Environment, FileSystemLoader
ghn = "TheLegendofAdlez_experimental"

levels = glob.glob(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\Content\*.Level.data"))

archetypes = []

print "Parsing levels..."

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

print "Parsing archetypes..."

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

print "Parsing Zilch scripts..."

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

print "Formatting tree..."

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

#pp = pprint.PrettyPrinter(indent=4)
#ppo = pp.pformat(arch_vars)
#with open("out.txt", "w") as outfile:
#    outfile.write(ppo)

print "Creating new Archetypes..."

arch_vars

print "Loading templates..."

env = Environment(loader=FileSystemLoader('templates'))
tpanel = env.get_template('TemplatePanel.z')
tpanelarch = env.get_template('TemplatePanel.z')

print "Rebuilding library..."

jinja_arches = []

for arch in arch_vars:
    _jarch = {}
    _jarch["name"] = arch
    _jarch["caps_name"] = arch.capitalize()
    _jvars = []
    for script in arch_vars[arch]:
        for var in script:
            siq = var[0] + "." + var[1]
            print "Building " + siq + "..."
            _jvar = {}
            _jvar["full"] = siq
            _jvar["local"] = var[1]
            if var[2] == "Real":
                _jvar["real"] = True
                _jvar["integer"] = False
                _jvar["bool"] = False
                _jvar["string"] = False
            elif var[2] == "Integer":
                _jvar["real"] = False
                _jvar["integer"] = True
                _jvar["bool"] = False
                _jvar["string"] = False
            elif var[2] == "String":
                _jvar["real"] = False
                _jvar["integer"] = False
                _jvar["bool"] = False
                _jvar["string"] = True
            elif var[2] == "Boolean":
                _jvar["real"] = False
                _jvar["integer"] = False
                _jvar["bool"] = True
                _jvar["string"] = False
            _jvars.append(_jvar)
    _jarch["vars"] = _jvars
    jinja_arches.append(_jarch)

#pp.pprint(jinja_arches)

print "Building PanelLogic.z..."

with open(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\PanelLogic.z"), "w") as zilchscript: #Content
    panel_result = tpanel.render(archetypes=jinja_arches)
    print panel_result
    zilchscript.write(panel_result)


print "Done!"

os.startfile(os.path.expanduser("~\Documents\GitHub\\" + ghn + "\THE GAME\PanelLogic.z"))

if False:
    answers = {}
    with open('avoid.csv', 'a') as csvfile:
        avoids = csv.writer(csvfile)
        for arch in arch_vars:
            viq = arch_vars[arch]
            for script in viq:
                for var in script:
                    siq = var[0] + "." + var[1]
                    print siq + " "
                    if not siq in answers:
                        ans = msvcrt.getch().upper()
                        answers[siq] = ans
                    if ans == "C":
                        avoids.writerow((var[0], var[1], var[2]))