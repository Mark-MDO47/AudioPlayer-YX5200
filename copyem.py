#
# copyem.py - copy files to newly formatted SD drive for YX5200
#    FAT32 formatted drive
#    note: filenames are of form ####_anything.wav
#          root directory needs ###.wav with no gaps
#
import os
import sys

theFnames = []
maxNum = 127  # beyond that is not currently used
fnameSilence = "0069__mdo47__silence.wav"  # to fill in gaps
theFrom = "D:/svnNew/SoundsSciFi/SoundsRecordedMDO/secondCut"
theSD = "H:"

for fname in os.listdir(theFrom):
    if (fname.lower().endswith(".wav")) and (maxNum >= int(fname[:4])):
        theFnames.append(fname.lower())
theFnames.sort()
theMaxNum = int(theFnames[-1][:4])

"""
for fname in theFnames:
   print("%s" % fname)
"""

# first the root directory
count = 1 # we do not want number 0 to be copied
for fname in theFnames:
    fcount = int(fname[:4])
    if fcount < count:
        continue # we do not want number 0 to be copied
    for idx in range(count, fcount):
        print("cp %s/%s %s/%03d.wav" % (theFrom, fnameSilence, theSD, idx))
    print("cp %s/%s %s/%03d.wav" % (theFrom, fname, theSD, fcount))
    count = fcount + 1

"""
# now the folders 01, 02 etc. Note that folder 00 is not used!!!
print(" ")
numFolders = 1 + theMaxNum // 10
for dir in range(1, 1 + numFolders):
    print("mkdir %s/%02d" % (theSD, dir))
    count = minFnum = 1 + 10 * (dir - 1)
    maxFnum = minFnum + 8
    for fname in theFnames:
        fcount = int(fname[:4])
        if fcount < minFnum:
            continue
        for idx in range(count, min(fcount, maxFnum+1)):
            print("cp %s/%s %s/%02d/%03d.wav" % (theFrom, fnameSilence, theSD, dir, idx))
        if fcount <= maxFnum:
            print("cp %s/%s %s/%02d/%03d.wav" % (theFrom, fname, theSD, dir, fcount))
        count = fcount + 1
        if fcount >= maxFnum:
            break

# now the MP3 folder
print(" ")
print("mkdir %s/MP3" % theSD)
for fname in theFnames:
    fcount = int(fname[:4])
    print("cp %s/%s %s/MP3/%04d.wav" % (theFrom, fname, theSD, fcount))
"""

# now the attributions
print(" ")
print("mkdir %s/ATTRIBUTIONS" % theSD)
print("cp  %s/Attributions.html %s/ATTRIBUTIONS" % (theFrom, theSD))
