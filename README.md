# AudioPlayer-YX5200
Easy method to reliably use the YX5200 Audio Player module.

These routines were developed by me for the Rubber Band Gun
* https://github.com/Mark-MDO47/RubberBandGun

![alt text](https://github.com/Mark-MDO47/RubberBandGun/blob/master/PartsInfo/YX5200_MP3player.png "Top view pin arrangement on YX5200 module")
![alt text](https://github.com/Mark-MDO47/RubberBandGun/blob/master/PartsInfo/YX5200_MP3player_pinouts.png "Description of pins on YX5200 module")

The YX5200 uses FAT32-formatted TF or microSD card up to 32 GByte.

Files to help with using YX5200 can be found here:
* https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
* https://github.com/DFRobot/DFRobotDFPlayerMini

These look like a helpful sites for the YX5200:
* https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
* https://github.com/DFRobot/DFRobotDFPlayerMini

# My Experiences

Here is a description of my experiences using the YX5200 module (I had some challenges)

YX5200 module works nicely; it does not require a separate programmer and can play MP3 files. *.wav file start faster after a command so I used those instead, but it depends on what your project is for as to what file format you would use.

You definitely want to use the 1K resistor on the TX line or you can distinctly hear clicks during serial communication.

My experience:
- Using .playMp3Folder() worked on the first few calls but I had trouble making it work when interrupting a playing sound. I tried a bunch of things (but not every combination) and finally gave it up and now use the most basic of functions .play().
- While doing the above experiments I had the impression that turning ACK on (default at this time) made it more likely to have the trouble above. I turned ACK off in the .begin(mySoftwareSerial, false, true) call.
- Sometimes there was a delay in the BUSY pin registering after starting a sound. So far all the delays I have documented were <= 40 milliseconds. Since my code wants to do things (LED-related) faster than that, I put in code to force a fake BUSY for the first 250 milliseconds after starting a sound. Probably overkill.
- Some of my readings indicate that there are knock-off clones of the YX5200 module that may not implement all the functions properly. My guess would be that they have an out-of-date set of firmware. At least some of these clones used a red LED to indicate sound playing instead of the blue LED used on the genuine YX5200. My modules did have a blue LED, but this is not necessarily a guarantee that they were genuine, so it is possible the problems I had were due to using a knock-off clone.

Extras:

Check out https://https://github.com/PowerBroker2/DFPlayerMini_Fast for a re-write (much simplified) of the DFRobot routines. I continued using the DFRobot routines for this project since by the time I found the other I had a lot of experience with the DFRobot routines.

That area also includes the PDF file I copied into my YX5200_info/ directory above; that is the best information on the chip that forms the basis of the YX5200 module that I have seen.

