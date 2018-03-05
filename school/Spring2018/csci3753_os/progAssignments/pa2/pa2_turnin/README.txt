Name: Anthony Tracy

I have three other files in this folder:

  1. Makefile - 
     Just using the made -C ... command will make the helloworld module and the simple_char_driver
     Note that since the helloworld.c script is not in this file then the line -m for the helloworld
     will also need to be commented out. Also I have a PA2_simple_char_driver.o and ..2.o in this make file
     this is because I broke the first file and rather than erase it I used it as a reference and made a new one.
     Mianly it was not dynacmic and was giving me trouble with making the device file within the main driver
     script.

  2. test_PA2_simple_char_driver2.c - 
     Note this has a 2 at the end because I again broke my first one and didnt want to rename everything once I
     actually got it working.
     This file can be compiled and run without giving any special commands. Once running it asks user questions
     and reads/writes/seeks in the device file.

  3. PA2_simple_char_driver2.c - 
     This is my implimentations, sorry for the sloppy code, I am still getting used to c since it has been a while,
     and printf and scanf make my life difficult,
     This file does not build the dev file on initiation - I tried it didn't like it, hence driver2. Anyway inorder
     to test this, the command needs to be run:

       “sudo mknod -m 777 /dev/PA2_simple_character_device2 c 262 0”
  
     Note that the nejor number is 262, this was free on my system. If changed I do not have the code automated to
     correct for this which I again tried and couldn't quite figure it out...


