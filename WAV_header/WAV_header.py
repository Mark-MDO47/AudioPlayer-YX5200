# WAV_header.py - read and check the WAV/RIFF header for use on WX5200
# Author: Mark Olson 2023-05-29
#
# References:
#    http://www.topherlee.com/software/pcm-tut-wavformat.html
#    https://ccrma.stanford.edu/courses/422-winter-2014/projects/WaveFormat/
#    http://netghost.narod.ru/gff/graphics/summary/micriff.htm
#    https://github.com/Mark-MDO47/AudioPlayer-YX5200
#
# 0         4   ChunkID          Contains the letters "RIFF" in ASCII form
#                                (0x52494646 big-endian form).
# 4         4   ChunkSize        36 + SubChunk2Size, or more precisely:
#                                4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
#                                This is the size of the rest of the chunk 
#                                following this number.  This is the size of the 
#                                entire file in bytes minus 8 bytes for the
#                                two fields not included in this count:
#                                ChunkID and ChunkSize.
# 8         4   Format           Contains the letters "WAVE"
#                                (0x57415645 big-endian form).
#
# The "WAVE" format consists of two subchunks: "fmt " and "data":
# The "fmt " subchunk describes the sound data's format:
#
# 12        4   Subchunk1ID      Contains the letters "fmt "
#                                (0x666d7420 big-endian form).
# 16        4   Subchunk1Size    16 for PCM.  This is the size of the
#                                rest of the Subchunk which follows this number.
# 20        2   AudioFormat      PCM = 1 (i.e. Linear quantization)
#                                Values other than 1 indicate some 
#                                form of compression.
# 22        2   NumChannels      Mono = 1, Stereo = 2, etc.
# 24        4   SampleRate       8000, 44100, etc.
# 28        4   ByteRate         == SampleRate * NumChannels * BitsPerSample/8
# 32        2   BlockAlign       == NumChannels * BitsPerSample/8
#                                The number of bytes for one sample including
#                                all channels. I wonder what happens when
#                                this number isn't an integer?
# 34        2   BitsPerSample    8 bits = 8, 16 bits = 16, etc.
#           2   ExtraParamSize   if PCM, then doesn't exist
#           X   ExtraParams      space for extra parameters
#

import sys
# import string
import os
import argparse


###################################################################################
# little_endian_to_big_int - convert little-endian bytes to big-endian integer
#
def little_endian_to_big_int(inVal,numBytes):
    outVal = 0
    for i in range(numBytes):
        shift = 8*i
        outVal += inVal[i] << shift
    return outVal
        
###################################################################################
# do_WAV_header - read and parse WAV/RIFF header
#
# Assumes we are on an Intel Windows machine.
# Bytes are a mixture of little-endian and big-endian.
#
# Checks to see if this file is appropriate for use with WX5200 Audio Module
#
def do_WAV_header(wavFname):
    header = [] # little-endian
    wav_fmt = [
        [ 0, 4,"BE","STRMUSTBE","RIFF","ChunkID"],
        [ 8,12,"BE","STRMUSTBE","WAVE","Format"],
        [12,16,"BE","STRMUSTBE","fmt ","Subchunk1ID"],
        [16,20,"LE","INTMUSTBE",16,    "Subchunk1Size"],
        [20,22,"LE","INTMUSTBE", 1,    "AudioFormat"],
        [22,24,"LE","INTMUSTBE", 1,    "NumChannels"],
        [24,28,"LE","VALUE",    -1,    "SampleRate"],
        [34,36,"LE","INTMUSTBE",16,    "BitsPerSample"]
    ] # end wav_fmt[]
    wav_values = {
      "ChunkID": "",
      "Format": "",
      "Subchunk1ID": "",
      "Subchunk1Size": -1,
      "AudioFormat": -1,
      "NumChannels": -1,
      "SampleRate": -1,
      "BitsPerSample": -1
    } # end wav_values{}
    goodSampleRates = [22050, 44100, 48000] # work with YX5200

    
    try:
        fobj = open(wavFname, 'rb')
        header = fobj.read(36)
        fobj.close()
    except:
        sys.stderr.write("ERROR - could not open/read %s\n" % os.path.realpath(wavFname))
        return

    noGood = False
    for i in range(len(wav_fmt)):
        fmt = wav_fmt[i]
        val = header[fmt[0]:fmt[1]]
        if "LE" == fmt[2]:
            val = little_endian_to_big_int(val,fmt[1]-fmt[0])
        if "STRMUSTBE" == fmt[3]:
            val = val.decode()
            if fmt[4] != val:
                noGood = True
                print("ERROR: expecting WAV header bytes %d-%d to be %s not %s" % (fmt[0],fmt[1]-1,fmt[4],val))
        elif "INTMUSTBE" == fmt[3]:
            if fmt[4] != val:
                noGood = True
                print("ERROR: expecting WAV header bytes %d-%d to be %s not %s" % (fmt[0],fmt[1]-1,fmt[4],val))
        wav_values[fmt[5]] = val
    if wav_values["SampleRate"] not in goodSampleRates:
        noGood = True
        print("ERROR: expecting WAV header SampleRate to be one of %s not %s" % (goodSampleRates,wav_values["SampleRate"]))
    if noGood:
        print("\nERROR: WAV file not usable with YX5200 Audio Module")
    else:
        print("\nWAV file is usable with YX5200 Audio Module")
    print("\n%s" % wav_values)

###################################################################################
# "__main__" processing for WAV_header
#
# use argparse to process command line arguments
# python WAV_header.py -h to see what the arguments are
#
if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(prog='WAV_header',
        formatter_class=argparse.RawTextHelpFormatter,
        description="read and parse WAV/RIFF header to stdout - hex (little- and big-endian) plus interpretation",
        epilog="""Example:
python WAV_header.py myFile.wav
""",
        usage='%(prog)s wavFname wavFname')
    my_parser.add_argument('wavFname',type=str,help='path to wavFname text file, copied from Kindle book list')
    args = my_parser.parse_args()

    # all the real work is done here
    do_WAV_header(args.wavFname)

