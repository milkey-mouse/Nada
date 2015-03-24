from jinja2 import Environment, FileSystemLoader
import subprocess
import os.path
import shutil
from PIL import Image
import win32gui
import glob
import time
import uuid
import os
from subprocess import *

#TODO: Create new Zero template for sprite-based playback

#they said it couldn't be done
#and they were wrong!
#well, they said it couldn't be done *correctly*...
#so i guess not

#original_movie = "Countdown.wmv"

original_movie = "The Mysterious Floating Orb.mp4"

#original_movie = "London Brawling.mp4"

print "Located video file at " + original_movie

print "Deleting old frames..."

for old_frame in glob.glob("*.jpg"):
    os.remove(old_frame)

for old_frame in glob.glob("*.png"):
    os.remove(old_frame)

for old_audio in glob.glob("*.mp3"):
    os.remove(old_audio)

for old_video in glob.glob("*.avi"):
    os.remove(old_video)

for old_frame in glob.glob(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\") + "*.jpg"):
    os.remove(old_frame)

for old_meta in glob.glob(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\") + "*.jpg.meta"):
    os.remove(old_meta)

for old_frame in glob.glob(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\") + "*.png"):
    os.remove(old_frame)

for old_meta in glob.glob(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\") + "*.png.meta"):
    os.remove(old_meta)

for old_audio in glob.glob(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\") + "*.mp3"):
    os.remove(old_audio)

print "Extracting audio..."

subprocess.call("ffmpeg -i \"" + original_movie + "\" -vn -ar 44100 -ac 2 -ab 96k -f mp3 vid_sound.mp3")

print "Splitting into frames..."

subprocess.call("ffmpeg -i \"" + original_movie + "\" -r 24 frame%08d.png")

print "Optimizing frames..."

idx = 0

tasks = []

#judging by my experiments baseline is always better for this

#print "Generating progressive samples..."
#
#while True:
#    idx += 1
#    curpath = "frame" + str(idx).zfill(8) + ".png"
#    if not os.path.isfile(curpath):
#        break
#    print curpath.replace(".png", "_progressive")
#    tasks.append(subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\convert.exe\" -strip -resize 50% -gaussian-blur 0.08 -sampling-factor 4:2:0 -quality 80% -interlace Plane " + curpath + " " + curpath.replace(".png", "_progressive.jpg"))) # -define:extent=50000
#
#while len(tasks) > 0:
#    for task in tasks:
#        if not task.poll() == None:
#            tasks.remove(task)
#
#idx = 0
#
#print "Generating baseline samples..."
#
#while True:
#    idx += 1
#    curpath = "frame" + str(idx).zfill(8) + ".png"
#    if not os.path.isfile(curpath):
#        break
#    print curpath.replace(".png", "_baseline")
#    tasks.append(subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\convert.exe\" -strip -resize 50% -gaussian-blur 0.08 -sampling-factor 4:2:0 -quality 80% " + curpath + " " + curpath.replace(".png", "_baseline.jpg")))
#
#while len(tasks) > 0:
#    for task in tasks:
#        if not task.poll() == None:
#            tasks.remove(task)
#
#print "Selecting best versions..."
#
#idx = 0
#
#while True:
#    idx += 1
#    standard = "frame" + str(idx).zfill(8) + ".jpg"
#    baseline = "frame" + str(idx).zfill(8) + "_baseline.jpg"
#    progressive = "frame" + str(idx).zfill(8) + "_progressive.jpg"
#    print baseline
#    if not os.path.isfile(baseline):
#        break
#    b_size = os.path.getsize(baseline)
#    p_size = os.path.getsize(progressive)
#    if b_size > p_size:
#        print "b-" + str(b_size)
#        print "p-" + str(p_size)
#        shutil.copyfile(baseline, standard)
#    else:
#        print "b-" + str(b_size)
#        print "p-" + str(p_size)
#        shutil.copyfile(progressive, standard)

print "Calculating square sizes..."

resize = 0.5

side = str((Image.open("frame00000001.png").size[0] - Image.open("frame00000001.png").size[1]) * resize / 2)

pct_size = str(Image.open("frame00000001.png").size[0]) + "x" + str(Image.open("frame00000001.png").size[1])

print "Generating diff masks..."

#if only i had /dev/null as a service

#http://devnull-as-a-service.com/home/

idx = 0

with open(os.devnull, 'w') as tempf:
    while True:
        idx += 1
        curpath = "frame" + str(idx).zfill(8) + ".png"
        if not os.path.isfile(curpath):
            break
        if idx % 24 == 1:
            print curpath.replace(".png", "") + " - keyframe"
            nsp = subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\convert.exe\" -size " + pct_size + "x" + pct_size + " xc:white " + "mask" + str(idx).zfill(8) + ".png", stdout=tempf, stderr=tempf)
            #nsp.communicate()
            tasks.append(nsp)
        elif os.path.isfile("frame" + str(idx + 1).zfill(8) + ".png"):
            print curpath.replace(".png", "")
            nsp = subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\compare.exe\" -fuzz 5% frame" + str(idx - 1).zfill(8) + ".png frame" + str(idx).zfill(8) + ".png -compose Src -highlight-color White -lowlight-color Black omask" + str(idx).zfill(8) + ".png", stdout=tempf, stderr=tempf)
            #nsp.communicate()
            tasks.append(nsp)
        while len(tasks) > 50:
            for task in tasks:
                if not task.poll() == None:
                    tasks.remove(task)

    while len(tasks) > 0:
        for task in tasks:
            if not task.poll() == None:
                tasks.remove(task)

print "Dilating diff masks..."

idx = 0

with open(os.devnull, 'w') as tempf:
    while True:
        idx += 1
        curpath = "omask" + str(idx).zfill(8) + ".png"
        if not os.path.isfile(curpath):
            if os.path.isfile("omask" + str(idx + 1).zfill(8) + ".png"):
                continue
            else:
                break
        print curpath.replace(".png", "")
        nsp = subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\convert.exe\" omask" + str(idx).zfill(8) + ".png -blur 5x65000 -threshold 0 -fill white -opaque white mask" + str(idx).zfill(8) + ".png", stdout=tempf, stderr=tempf)
        tasks.append(nsp)
        while len(tasks) > 50:
            for task in tasks:
                if not task.poll() == None:
                    tasks.remove(task)

    while len(tasks) > 0:
        for task in tasks:
            if not task.poll() == None:
                tasks.remove(task)

print "Generating colored diffs..."

idx = 0

with open(os.devnull, 'w') as tempf:
    while True:
        idx += 1
        curpath = "frame" + str(idx).zfill(8) + ".png"
        if not os.path.isfile(curpath):
            break
        print curpath.replace(".png", "")
        nsp = subprocess.Popen("\"C:\Program Files\ImageMagick-6.8.9-Q16\convert.exe\" frame" + str(idx).zfill(8) + ".png mask" + str(idx).zfill(8) + ".png -alpha Off -compose CopyOpacity -strip -resize " + str(round(resize * 100)) + "% -quality 00 -composite final" + str(idx).zfill(8) + ".png", stdout=tempf, stderr=tempf)
        #nsp.communicate()
        tasks.append(nsp)
        while len(tasks) > 50:
            for task in tasks:
                if not task.poll() == None:
                    tasks.remove(task)

while len(tasks) > 0:
    for task in tasks:
        if not task.poll() == None:
            tasks.remove(task)

print "Optimizing colored diffs..."

#no borders this time

idx = 0

with open(os.devnull, 'w') as tempf:
    while True:
        idx += 1
        curpath = "final" + str(idx).zfill(8) + ".png"
        if not os.path.isfile(curpath):
            break
        print curpath.replace(".png", "")
        nsp = subprocess.Popen("optipng.exe " + curpath, stdout=tempf, stderr=tempf)
        tasks.append(nsp)
        while len(tasks) > 50:
            for task in tasks:
                if not task.poll() == None:
                    tasks.remove(task)

while len(tasks) > 0:
    for task in tasks:
        if not task.poll() == None:
            tasks.remove(task)

#no preview for this version

print "Calculating file size..."

size = 0

for frame in glob.glob("final*.png"):
    size += os.path.getsize(frame)

for audio in glob.glob("*.mp3"):
    size += os.path.getsize(audio)

print str(size / 1088576) + " megabytes"

print "Importing into test project..."

env = Environment(loader=FileSystemLoader('templates'))
vpresenter = env.get_template('VideoPresenter.z')
framemeta = env.get_template('FrameMetadata.png.meta')

with open(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\VideoPresenter.z"), "w") as zilchscript:
    result = vpresenter.render(framenum=str(len(glob.glob("final*.png"))))
    print result
    zilchscript.write(result) 
    zilchscript.close()

size_x = str(Image.open("final00000001.png").size[0])
size_y = str(Image.open("final00000001.png").size[1])
origin_x = str(Image.open("final00000001.png").size[0] / 2)
origin_y = str(Image.open("final00000001.png").size[1] / 2)

while True:
    idx += 1
    curpath = "final" + str(idx).zfill(8) + ".png"
    if not os.path.isfile(curpath):
        break
    print curpath.replace(".png", "")
    shutil.copyfile(curpath.replace("frame", "final"), os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\" + curpath))
    with open(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\" + curpath + ".meta"), "w") as metadata:
        result = framemeta.render(frameid=str(idx),resid=str(uuid.uuid4().get_hex().lower()[0:16]),framesizex=size_x,framesizey=size_y,frameoriginx=origin_x,frameoriginy=origin_y)
        print result
        metadata.write(result)
        metadata.close()
print "vid_sound.mp3"
shutil.copyfile("vid_sound.mp3", os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\Content\\vid_sound.mp3"))

print "Done!"

etc = size / 30922 / 60

#Test results:
#17749228 bytes
#574 seconds
#30922 bytes/second

print "Cleaning up..."

for old_frame in glob.glob("*.jpg"):
    os.remove(old_frame)

for old_frame in glob.glob("*.png"):
    os.remove(old_frame)

for old_audio in glob.glob("*.mp3"):
    os.remove(old_audio)

for old_video in glob.glob("*.avi"):
    os.remove(old_video)

time.sleep(2)

os.startfile(os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\LosslessVideoTest.zeroproj"))

#time.sleep(2)
#os.startfile("video.avi")

#print "Locating cache..."

#zengine_ui = subprocess.Popen(("C:\Program Files (x86)\ZeroEditor\ZeroEditor.exe", os.path.expanduser("~\Documents\GitHub\Nada\LosslessVideoTest\LosslessVideoTest.zeroproj")))
#time.sleep(3)
#zengine_ui.terminate()
#time.sleep(2)

#def all_subdirs_of(b='.'):
#  result = []
#  for d in os.listdir(b):
#    bd = os.path.join(b, d)
#    if os.path.isdir(bd): result.append(bd)
#  return result

#latest_subdir = max(all_subdirs_of(os.path.expanduser('~\AppData\Local\ZeroContent')), key=os.path.getmtime)

#print "Cache found in " + latest_subdir + "."

#print "Caching Zero texture files..."

#idx = 0

#tasks = []

#while True:
#    idx += 1
#    curpath = "frame" + str(idx).zfill(8) + ".jpg"
#    if not os.path.isfile(curpath):
#        break
#    print curpath.replace(".jpg", ".ztex")
#    tasks.append(subprocess.Popen(("\"C:\Program Files (x86)\ZeroEditor\Tools\ImageProcessor.exe", "-in \"" + os.path.abspath(curpath) + "\"", "-out " + latest_subdir + "\frame" + str(idx) + ".ztex")))
#    while len(tasks) > 10:
#        for task in tasks:
#            if not task.poll() == None:
#                tasks.remove(task)