/*
 * File: pager-lru.c
 * Author:       Andy Sayler
 *               http://www.andysayler.com
 * Adopted From: Dr. Alva Couch
 *               http://www.cs.tufts.edu/~couch/
 *
 * Project: CSCI 3753 Programming Assignment 4
 * Create Date: Unknown
 * Modify Date: 2012/04/03
 * Description:
 * 	This file contains an lru pageit
 *      implmentation.
 */

#include <stdio.h> 
#include <stdlib.h>
#include <limits.h>

#include "simulator.h"

void pageit(Pentry q[MAXPROCESSES]) { 
    
    /* This file contains the stub for an LRU pager */
    /* You may need to add/remove/modify any part of this file */

    /* Static vars */
    static int initialized = 0;
    static int tick = 1; // artificial time
    static int timestamps[MAXPROCESSES][MAXPROCPAGES];

    /* Local vars */
    int proctmp;
    int pagetmp;

    /* initialize static vars on first run */
    if(!initialized){
	for(proctmp=0; proctmp < MAXPROCESSES; proctmp++){
	    for(pagetmp=0; pagetmp < MAXPROCPAGES; pagetmp++){
		timestamps[proctmp][pagetmp] = 0; 
	    }
	}
	initialized = 1;
    }
    
    /* TODO: Implement LRU Paging */
    int lru_pg, min_t;
    for(proctmp=0; proctmp < MAXPROCESSES; proctmp++){    // Loop through all processes - need to see which are active 
        if(q[proctmp].active) {                           // Make sure that the process is active before wasting time on it:
            pagetmp = q[proctmp].pc/PAGESIZE;             // Get page
            if(!q[proctmp].pages[pagetmp]) {              // Is page swapped in? - after this we assume no
                if(!pagein(proctmp,pagetmp)) {            // Now check if we can page it in - after this line assume we don't
                    min_t = INT_MAX;      // Start at largest possible number...
                    int pg_rem;         // This will be a holder for LRU process
                    for(pg_rem = 0; pg_rem < q[proctmp].npages; pg_rem ++) { // Look through everything for lowest timestamp... costly
                        if(timestamps[proctmp][pg_rem] < min_t) {
                            min_t = timestamps[proctmp][pg_rem];
                            lru_pg = pg_rem;
                        } // End of checking for Least used
                    } // End of looking through all processes to remove - though i wonder if I couldn't do this all at once...
                    
                    /* Know the page to swap out...*/
                    if(pageout(proctmp,lru_pg)) {          // Make  sure pageout returns true
                        pagein(proctmp,pagetmp);           // Having removed the lru_pg now add the current page (pagetmp)
                        timestamps[proctmp][lru_pg] = tick; // Make sure to update the clock on lru page
                    } // End of makeing a pageout
                } // End of check if we can even page in
            } // End of if page is loaded - paged in
        } // End if process is active
        timestamps[proctmp][pagetmp] = tick;               // Make sure to update all active pages
    } // End of checking all processes
    
    //fprintf(stderr, "pager-lru not yet implemented. Exiting...\n");
    //exit(EXIT_FAILURE);

    /* advance time for next pageit iteration */
    tick++;
} 
