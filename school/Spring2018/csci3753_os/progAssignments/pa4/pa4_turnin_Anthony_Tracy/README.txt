# Name: Anthony Tracy
# Assignment: PA 4


In this folder I have 3 files:
  1. Makefile - This is just the generic Makefile that came with the assignment, it worked by itself and I didn't add
  files to the project so I made no changes here.

  2. pager-lru.c - This is my implimentation of LRU just a timer (really just a ++ counter, but same idea)

  3. pager-predict.c - The only difference currently between this and a regular LRU is that I have it trying 
  to add more pages per process than just the 1 page requested. Having knowledge about the code being processed
  I know that it will all be linearly input, so I make the assumption that each page (in the table) will likely 
  be called in a somewhat linear fashion.
    - Things I mean to impliment :
      a. Since I noticed for loops I realized I should likely have the pager algorithm check if the page being 
      loaded is at the end of the page table, if so, I could then instead load the first page. This ideally 
      could be done with a slight change to my current code - by adding an if (lru_pg + i mod MAXPAGESIZE) 
      then load the page of the remander of the mod else just load lru_page + i.
      b. Then I also want to impliment buffering, I think it would save a lot of time to make sure there is always 
      some threshold of the data being paged out so that the pagin is only of cost "100" not "200" Since I would 
      need to both pageout and pagein on the spot. This couild be done with another condition and loop saying to 
      remove a remainder of a mod, for the number of pages allocated above some threashold.


As for building and running these you will need the full project from: https://github.com/asayler/CU-CS3753-2012-PA4
  NOTE: When doing this there is an error in the code, on line 68 of simulator.c the line should have a static inline void.
  1. Once the full project is downloaded move my files ( my makefile or not since it should be the same) into 
  the same directory
  2. run make in terminal
  3. test both lru and predictive with the following commands in terminal:
     a. ./test-lru
     b. ./test-predict

 
 
