#
# copyem.py - copy files to newly formatted SD drive for YX5200
#    FAT32 formatted drive
#    note: filenames are of form ####_anything.wav
#          root directory needs ###.wav with no gaps
#
import os
import sys
import argparse

theFnames = []
maxNum = 127  # beyond that is not currently used
# fnameSilence = "0069__mdo47__silence.wav"  # to fill in gaps
# theFrom = "D:/svnNew/SoundsSciFi/SoundsRecordedMDO/secondCut"
# theSD = "H:"

def doCopyem(theFrom = None, theSD = None, fnameSilence = None, copyCmd = None):
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
            print("%s %s/%s %s/%03d.wav" % (copyCmd, theFrom, fnameSilence, theSD, idx))
        print("%s %s/%s %s/%03d.wav" % (copyCmd, theFrom, fname, theSD, fcount))
        count = fcount + 1

    # now the attributions
    print(" ")
    print("mkdir %s/ATTRIBUTIONS" % theSD)
    print("%s  %s/Attributions.html %s/ATTRIBUTIONS" % (copyCmd, theFrom, theSD))


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='copyem',
        formatter_class=argparse.RawTextHelpFormatter,
        description="stdout receives list of copy commands for freshly formatted SD card",
        epilog="""Example:
python copyem.py -d ./myAudioFiles -s H: -f soundsOfSilence.wav --linux
""",
        usage='%(prog)s {-d directory -s sd-disk -f fname-silence {-l linux | -w windows} }')
    my_parser.add_argument('-d', '--directory', type=str, help='path to directory containing *.wav files', action='store', default="D:/svnNew/SoundsSciFi/SoundsRecordedMDO/secondCut")
    my_parser.add_argument('-s', '--sd-disk', type=str, help='path to freshly formatted FAT32 SD disk (e.g. H:)', action='store', default="H:")
    my_parser.add_argument('-f', '--fname-silence', type=str, help='filename to use as silence when break in numerical sequence', action='store', default="0069__mdo47__silence.wav")
    my_parser.add_argument('-w', '--windows', help='Use *.bat copy commands for output file', action='store_true')
    my_parser.add_argument('-l', '--linux', help='use *.sh cp commands for output file', action='store_true')
    args = my_parser.parse_args()

    copyCmd = None
    if args.windows:
        copyCmd = "copy"
    else:
        copyCmd = "cp"

    doCopyem(theFrom=args.directory, theSD=args.sd_disk, fnameSilence=args.fname_silence, copyCmd = copyCmd)
