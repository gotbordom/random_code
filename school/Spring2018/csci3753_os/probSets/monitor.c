// Name: Anthony Tracy


// Note this is still psudocode, there is implimentation of C for most part, but still psudocode

// This would be code found in a fucntion that the process would fork()

// Let there be some shared data as shown below:

MAX_THREAD=4;
AT_BARRIER=0;

/*


This is some section of code that each 
thread would be running and 
depending on the data
this will take a different
amount of time for each.


*/

// At this point we need the barrier:

lock();
  AT_BARRIER++; // Critical section, need mutex or the lock
signal()
  while(AT_BARRIER<=MAX_THREAD)
  {
    wait();  // we can now unlock the barrier;
  }

/*

This is the section that 4 processes
must be ready before we start this part.

*/
