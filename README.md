# AudioPlayer-YX5200
Easy method to reliably use the YX5200 Audio Player module.

These routines were developed by me for the Rubber Band Gun (RBG) project.
* https://github.com/Mark-MDO47/RubberBandGun

The YX5200 module can be found here
* https://smile.amazon.com/Anmbest-YX5200-DFPlayer-Supporting-Arduino/dp/B07JGWMPTF/

![alt text](https://github.com/Mark-MDO47/RubberBandGun/blob/master/PartsInfo/YX5200_MP3player.png "Top view pin arrangement on YX5200 module")
![alt text](https://github.com/Mark-MDO47/RubberBandGun/blob/master/PartsInfo/YX5200_MP3player_pinouts.png "Description of pins on YX5200 module")

The YX5200 uses FAT32-formatted TF or microSD card up to 32 GByte.

Files to help with using YX5200 can be found here:
* https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
* https://github.com/DFRobot/DFRobotDFPlayerMini

Best datasheet I could find on the YX5200 chip is found here
* https://github.com/PowerBroker2/DFPlayerMini_Fast/blob/master/extras/FN-M16P%2BEmbedded%2BMP3%2BAudio%2BModule%2BDatasheet.pdf

# My Experiences

Here is a description of my experiences using the YX5200 module (I had some challenges)

You definitely want to use the 1K resistor on the TX line or you can distinctly hear clicks during serial communication.

My experience (these comments apply to the modules I used, which had a chip labelled MH-ETLIVE MH2024K-24SS):
- Using .playMp3Folder() worked on the first few calls but I had trouble making it work when interrupting a playing sound. I tried a bunch of things (but not every combination) and finally gave it up and now use the most basic of functions .play().
  - Also *.wav files start faster after a command to play. Apparently there is some overhead to start an *.mp3 file. It was a small delay but noticeable in the RBG project.
  - Because the .play() function requires specific filenames and orders of file copies, I wrote copyem.py to help me get the files into the SD card in the correct order.
- While doing the above experiments I had the impression that turning ACK on (default at this time) made it more likely to have the trouble above. I turned ACK off in the .begin(mySoftwareSerial, false, true) call.
- Sometimes there was a delay in the BUSY pin registering after starting a sound. So far all the delays I have documented were <= 40 milliseconds. Since my code wants to do things (LED-related) faster than that, I put in code to force a fake BUSY for the first 250 milliseconds after starting a sound. Probably overkill.
- Some of my readings indicate that there are knock-off clones of the YX5200 module that may not implement all the functions properly. My guess would be that they have an out-of-date set of firmware. At least some of these clones used a red LED to indicate sound playing instead of the blue LED used on the genuine YX5200. My modules did have a blue LED, but this is not necessarily a guarantee that they were genuine, so it is possible the problems I had were due to using a knock-off clone.
- Both grounds on the YX5200 are marked as digital ground, but I found that if I connected them together the line output had a buzz (didn't hear it on speaker output). I got better results when I pretended that the GND between SPK1 and SPK2 was an analog ground.

There have been a lot of reactions to clone modules and difficulties with serial communication and audio noise. Here is an excellent resource on this subject

https://www.thebackshed.com/forum/ViewTopic.php?TID=11977&P=1

# copyem.py

This is a routine that makes it much easier to create SD cards that work with the .play() routine. Below is the help text from copyem.py.

Note: I run this routine in GIT bash on Windows 10, so I use the H: (or other letter) to access the drive but use the / separator for directories.

![alt text](https://github.com/Mark-MDO47/AudioPlayer-YX5200/blob/master/images/CopyemHelp.png "Help text for copyem.py")

It is OK to copy to the SD card using names like 001_this_is_a_test.wav, but if the names get longer than 8.3 then the directory gets more complicated and it might affect the speed of starting a sound eventually, so I just copied the number such as 001.wav.

So the sequence is:
- Put your ####*.wav files in a directory. For this example I will use the directory ./myAudioFiles
- - NOTE: I use # to indicate a decimal digit from 0 through 9
- Also make a ####*.wav file that is just a second or two of silence and place that in ./myAudioFiles
- Optionally make a Attributions.html file for attributions and place that in ./myAudioFiles
- Connect an SD-card that is 32 gigabytes or less and FAT-32 format the SD-card. In this example it will be on H:
- - NOTE: it MUST be freshly FAT-32 formatted; do not try to re-use SD card without formatting. There are many ways to do this; I use https://www.sdcard.org/downloads/formatter/

At this point, ./myAudioFiles has the following (short list of *.wav to make it readable)
- 0001_first.wav
- 0003_third.wav
- 0005_silence.wav
- Attributions.html

Run the program as follows
- python copyem.py -d ./myAudioFiles -s H: -f 0005_silence.wav > mycopy.sh

It will output the following (note: a blank line before attribution is omitted here)
- cp ./myAudioFiles/0001_first.wav H:/001.wav
- cp ./myAudioFiles/0005_silence.wav H:/002.wav
- cp ./myAudioFiles/0003_third.wav H:/003.wav
- cp ./myAudioFiles/0005_silence.wav H:/004.wav
- cp ./myAudioFiles/0005_silence.wav H:/005.wav
- mkdir H:/ATTRIBUTIONS
- cp  ./myAudioFiles/Attributions.html H:/ATTRIBUTIONS

Alternatively, "python copyem.py -d ./myAudioFiles -s H: -f 0005_silence.wav --windows > mycopy.bat" will output the following
- copy .\myAudioFiles\0001_first.wav H:\001.wav
- copy .\myAudioFiles\0005_silence.wav H:\002.wav
- copy .\myAudioFiles\0003_third.wav H:\003.wav
- copy .\myAudioFiles\0005_silence.wav H:\004.wav
- copy .\myAudioFiles\0005_silence.wav H:\005.wav
- mkdir H:\ATTRIBUTIONS
- copy  .\myAudioFiles\Attributions.html H:\ATTRIBUTIONS

Then either source mycopy.sh or run mycopy.bat, eject the SD card, and insert it into the YX5200.

# Extras:

## Rewrite of DFRobot routines
Check out https://https://github.com/PowerBroker2/DFPlayerMini_Fast for a re-write (much simplified) of the DFRobot routines. I continued using the DFRobot routines for this project since by the time I found the other I had a lot of experience with the DFRobot routines.

## Sound output is surprisingly good - maybe use Bluetooth speaker?
This module puts out really good sound. On the RBG project, the speaker just wasn't good enough to show off the sound, so I added a KCX_BT_EMITTER module and connected to a powered Bluetooth speaker. Sounds fantastic!

See here for programming the KCX_BT_EMITTER to auto-connect to your speaker:
- https://github.com/Mark-MDO47/BluetoothAudioTransmitter_KCX_BT_EMITTER

See here for a schematic showing the YX5200 connected to the KCX_BT_EMITTER. Note the connection to the KCX_BT_EMITTER AGND (audio or analog ground).
- https://github.com/Mark-MDO47/RubberBandGun/blob/master/RubberBandGun_Wiring.pdf
