from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
import glob
import os

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

#this messy code below takes each line and scrolls up until it finds a parent (one with a colon at the end and with a lower number of tabs)
#and sorts then into lists in a dict, with the multi-level ones being handled by linking.

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

print "Grabbing images..."

linedict = defaultdict(lambda:[])

images = {}

for parent in linetree:
    for item in linetree[parent]:
        if "~" in item:
            name = item.split("~")[0]
            image = item.split("~")[1]
            if image.endswith(":"):
                name += ":"
                image = image[:-1]
            uid = ""
            try:
                with open(glob.glob(os.path.expanduser("~\\Documents\\GitHub\\TheLegendofAdlez\\THE GAME\\Content\\" + image + ".*.meta"))[0], "r") as metafile:
                    meta = metafile.read()
                    metas = meta.split("\n")
                    for levelln in metas:
                        cln = levelln.replace("\t", "")
                        if cln.startswith("string Name = "):
                            uid = cln.replace("\"", "").replace("string Name = ", "").replace(",", "")
                        if cln.startswith("uint64 ResourceId = "):
                            uid = cln.replace("uint64 ResourceId = ", "").replace(",", "") + ":" + uid
                            break
            except:
                uid = name
            images[name] = uid
            linedict[parent].append(name)
        else:
            linedict[parent].append(item)

print images


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
                try:
                    for small_item in linedict[item]:
                        formatted.append(("4e7bac697bec55c5:Verdana", 45, white, small_item))
                except:
                    pass
            else:
                formatted.append(("4e7bac697bec55c5:Verdana", 45, white, item.replace(":", "")))
    else:
        formatted.append((font, size, color, "")) #buffer
        formatted.append((font, size, color, text))
        formatted.append((font, size, color, "")) #buffer

print "Compiling level..."

env = Environment(loader=FileSystemLoader('templates'))
level_template = env.get_template('CreditsLevelTemplate.Level.data')

jinjadict = []

imgdict = []

uid = 6

pos = 0.0

sign = ""

for item in formatted:
    if item[0] == "54136df68d049509:Triforce":
        pos -= 1.5
    elif item[0] == "53f62bf3a4deae78:wendy":
        pos -= 0.5
    jinjadict.append({"font":item[0],"size":item[1],"red":item[2][0],"green":item[2][1],"blue":item[2][2],"text":item[3].replace("\"", "'"),"uid":str(uid),"pos":str(pos)})
    if item[3] in images:
        print item[3]
        if sign == "":
            sign = "-"
        else:
            sign = ""
        uid += 1
        imgdict.append({"side":sign,"pos":str(pos),"uid":str(uid),"id":images[item[3]]})
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

print imgdict

with open(os.path.expanduser("~\Documents\GitHub\TheLegendofAdlez\THE GAME\Content\Credits.Level.data"), "w") as levelfile:
    level_result = level_template.render(nodes=jinjadict,last=jinjadict[-1]["pos"],images=imgdict)
    print level_result
    levelfile.write(level_result)
    levelfile.close()