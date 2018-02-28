Name: Anthony Tracy
Email: antr9811@colorado.edu

Files in this submission:

1. simple_add.c
  - This file contains the c code to create a system call.
    This system call takes 3 arguments:
      - int a   : a standerd intiger number
      - int b   : a standerd intiger number
      - int *loc: a dereferenced point - space for an intiger number
  - This function writes a+b to the address located at loc
    then it writes to the system log, a standerd message, that says
    the values where added to make another value and the address 
    that it was written to. If all is successful, it returns 0.
  - This would be located under the syscall portion of the build within the kernal.

2. userspace.c
  - This takes no imputs. It is just a main function that declares 3 ints a, b, and loc.
    This then calls the syscall with a, b, and &loc.
  - Then it prints to the screen information that can be verified with the syslog which is
    written to due to the printk in the simple_add syscall.
  - This also tests the helloworld.c syscall.

3. Makefile
  - This file is the script that actually starts the build. The make file defines 
    how and in what order to build everything.
  - This is would be the top of the build tree (if I am thinking of 'build tree' in
    the sense that you mean the order in which the kernal is compiled).

4. syscall_64.tbl
  - this file contains the syscall table. Which is referenced by the OS inorder to 
    load the correct syscall when needed. 
  - This file is just a table file and is made with the syscalls. Each syscall
    needs to be referenced in this file.
5. include/linux/syscalls.h
  - This file contains the header file for all of the c programs that were written for syscalls.
  - This is also needs to be updated in the build with each syscall that is made. Then
    whenever a new syscall is added the whole kernel needs to be re-compiled.

6. syslog
  - This is a log file that the OS writes update infromation to. So whenever printk is called the
    data is written to the log file.
  - This is made after the build is complete and is used to write system infromation to.

Using and Testing simple_add.c:

  - Since int *loc is the pointer to the location of storing the sum of a+b, then the input must also 
    be a pointer. In order to test this with the userspace.c code, the ints a and b can be changed
    then I compile the code and run the executable file.


