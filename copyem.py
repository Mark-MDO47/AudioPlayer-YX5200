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

def doCopyem(theFrom = None, theSD = None, fnameSilence = None, copyCmd = None, theSlash = None, noAttributeFile = False):
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
            print("%s %s%s%s %s%s%03d.wav" % (copyCmd, theFrom, theSlash, fnameSilence, theSD, theSlash, idx))
        print("%s %s%s%s %s%s%03d.wav" % (copyCmd, theFrom, theSlash, fname, theSD, theSlash, fcount))
        count = fcount + 1

    # now the attributions
    if False == noAttributeFile:
        print(" ")
        print("mkdir %s%sATTRIBUTIONS" % (theSD, theSlash))
        print("%s  %s%sAttributions.html %s%sATTRIBUTIONS" % (copyCmd, theFrom, theSlash, theSD, theSlash))


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='copyem',
        formatter_class=argparse.RawTextHelpFormatter,
        description="stdout receives list of copy commands for freshly formatted SD card",
        epilog="""copyem.py is used to copy consecutive *.wav files to a newly formatted TF or SD card for YX5200 Audio Module
The source files in the --directory area DIRECTORY are of format ####*.wav where # = decimal digit.
By default the file Attributions.html in DIRECTORY will be stored on SD card in the ATTRIBUTIONS/ directory.
When using the .play() method, the files must be of form ###.ext (ext=wav, mp3, etc.) and must be copied in order.
copyem.py uses *.wav files but YX5200 can use other formats too.
If there are SD card files 001.wav and 003.wav, there must be a 002.wav or .play() will find the wrong file. copyem.py takes care of that.
Example:
python copyem.py -d ./myAudioFiles -s H: -f 0070_soundsOfSilence.wav --linux
""",
        usage='%(prog)s {-d directory -s sd-disk -f fname-silence {-l linux | -w windows} }')
    my_parser.add_argument('-d', '--directory', type=str, help='path to directory containing *.wav files', action='store', default="D:/svnNew/SoundsSciFi/SoundsRecordedMDO/secondCut")
    my_parser.add_argument('-s', '--sd-disk', type=str, help='path to freshly formatted FAT32 SD disk (e.g. H:)', action='store', default="H:")
    my_parser.add_argument('-f', '--fname-silence', type=str, help='filename within DIRECTORY to use as silence when break in numerical sequence', action='store', default="0069__mdo47__silence.wav")
    my_parser.add_argument('-w', '--windows', help='Use *.bat copy commands for output file', action='store_true')
    my_parser.add_argument('-l', '--linux', help='use *.sh cp commands for output file', action='store_true')
    my_parser.add_argument('-n', '--no-attribute-file', help='do not include Attributions.html from DIRECTORY in an ATTRIBUTIONS directory on the sd-disk', action='store_true', default=False)
    args = my_parser.parse_args()

    copyCmd = None
    if args.windows:
        copyCmd = "copy"
        theSlash = "\\"
        args.directory = args.directory.replace("/",theSlash)
    else:
        copyCmd = "cp"
        theSlash = "/"
        args.directory = args.directory.replace("\\",theSlash)

    doCopyem(theFrom=args.directory, theSD=args.sd_disk, fnameSilence=args.fname_silence, copyCmd = copyCmd, theSlash = theSlash, noAttributeFile = args.no_attribute_file)
