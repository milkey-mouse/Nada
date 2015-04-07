from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
import os, sys

credits = ""

print "Getting lines..."

with open(os.path.expanduser("~\\Documents\\GitHub\\TheLegendofAdlez\\Credits.txt"), "r") as creditsfile:
    credits = creditsfile.read()

lines = []

for line in credits.splitlines():
    stripped = line.lstrip()
    if stripped == "":
        continue
    spaces = len(line) - len(stripped)
    lines.append((stripped.rstrip(), spaces))

print "Assembling hierarchy..."

linetree = defaultdict(lambda:[]) #constructs a dict full of lists so .append() will never fail

for idx in range(0, len(lines) - 1):
    line = lines[idx]
    sidx = idx
    while not sidx == 0:
        sidx -= 1
        if lines[sidx][0].endswith(":") and (lines[sidx][1] < lines[idx][1]):
            linetree[lines[sidx][0]].append(lines[idx][0])
            break
    if sidx == 0:
        linetree[""].append(lines[idx][0])

linedict = {}

for i in linetree:
    linedict[i] = linetree[i]


print "Formatting text..."

formatted = []

#(font, size, text)


#color palette
green = (0,1,0)
gold = (0.862745,0.690196,0.227450)
white = (1,1,1)

for tag in linedict[""]:
    font = "4e7bac697bec55c5:Verdana"
    size = 45
    color = white
    text = tag
    if tag.endswith(":"):
        font = "54136df68d049509:Triforce"
        size = 100
        color = green
        formatted.append((font, size, color, tag.replace(":", "")))
        for item in linedict[tag]:
            if item.endswith(":"):
                formatted.append(("53f62bf3a4deae78:wendy", 70, gold, item.replace(":", "")))
                for small_item in linedict[item]:
                    formatted.append(("4e7bac697bec55c5:Verdana", 45, white, small_item))
            else:
                formatted.append(("4e7bac697bec55c5:Verdana", 45, white, item.replace(":", "")))
    else:
        formatted.append((font, size, color, "")) #buffer
        formatted.append((font, size, color, text))
        formatted.append((font, size, color, "")) #buffer

print "Compiling level..."

for tag in formatted:
    print tag

#sys.exit(0)

env = Environment(loader=FileSystemLoader('templates'))
level_template = env.get_template('CreditsLevelTemplate.Level.data')

jinjadict = []

uid = 5

pos = 0.0


for item in formatted:
    if item[0] == "54136df68d049509:Triforce":
        pos -= 1.5
    elif item[0] == "53f62bf3a4deae78:wendy":
        pos -= 0.5
    jinjadict.append({"font":item[0],"size":item[1],"red":item[2][0],"green":item[2][1],"blue":item[2][2],"text":item[3].replace("\"", "'"),"uid":str(uid),"pos":str(pos)})
    if item[0] == "54136df68d049509:Triforce":
        pos -= 2
    elif item[0] == "4e7bac697bec55c5:Verdana":
        if not item[3] == "":
            pos -= 1
        else:
            pos -= 0.25
    elif item[0] == "53f62bf3a4deae78:wendy":
        pos -= 1.5
    uid += 1

print jinjadict

with open(os.path.expanduser("~\Documents\GitHub\TheLegendofAdlez\THE GAME\Content\Credits.Level.data"), "w") as levelfile:
    level_result = level_template.render(nodes=jinjadict,last=jinjadict[-1]["pos"])
    print level_result
    levelfile.write(level_result)
    levelfile.close()