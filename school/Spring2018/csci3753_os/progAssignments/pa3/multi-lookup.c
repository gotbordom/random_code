#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include "util.h"
//#include "multi-lookup.h"

// gcc -pthread -o multi-lookup multi-lookup.c -I .



//MODULE_LICENSE("GPL");  // Not sure I reallllly need this for class but hey why not.
//MODULE_AUTHOR("Anthony Tracy");
//MODULE_DESCRIPTION("OS PA3: writing a script to create threads and loopup ip addresses");
//MODULE_VERSION("0.1");

/* ------------Struct Methods --------------- */
/* Semaphores */


//void wait(struct semaphore *S);
//void signal(struct semaphore *S);
//void init_semaphore(semaphore *S,int n,int buffer);
//void dest_semaphore(semaphore *S)


/* ------------Data structs------------------ */

typedef struct{
  int max,items,isComplete;
  int head, tail;       // Need these locations
  int full, empty;      // want to know for signaling
  pthread_mutex_t *mut; // Make sure to have a lock for accessing this buffer
  pthread_cond_t *notFull, *notEmpty; // Make sure to have conditions to signal on
  char **string;
} buffer;


typedef struct{
  buffer *b;            // Also need to pass the shared q to all threads
  FILE *fHandles;      // pointer to a string - the filename to read
  pthread_mutex_t *threadLock;  // Locking when thread writes to logs
  int serviced;           // want the number of lines 
  //int isComplete;     // Are the files done being read or not (1) true (0) false - bit map would save space...
} threadData;


/* Queues */
threadData *threadDataInit(buffer *b,FILE *fHandle);
void threadDataDelete(threadData *b);

buffer *bufferInit(int size);
void bufferDelete(buffer *b);
void bufferAdd(buffer *b, char *element);
void bufferRem(buffer *b);
char *front(buffer *b);



/* ------------Methods----------------------- */

// threadData methods:
threadData *threadDataInit(buffer *b,FILE *fHandle){
  threadData *p;
  p = (threadData *)malloc(sizeof(threadData));
  p->b = b;
  p->serviced = 0;
  p->fHandles = fHandle;
  p->threadLock=(pthread_mutex_t*)malloc(sizeof(pthread_mutex_t));
  pthread_mutex_init(p->threadLock,NULL);
  //p->items=numFiles;
  return p;
}
void threadDataDelete(threadData *p){
 //bufferDelete(p->q);
 //free(p->isComplete);
 pthread_mutex_destroy(p->threadLock);
 free(p->threadLock);
 free(p);
}

// buffer methods:
buffer *bufferInit(int size){
  buffer *b;
  b = (buffer *)malloc(sizeof(buffer));

  b->string = (char**)malloc(sizeof(char*)*size);
  b->max=size;
  b->isComplete=0;
  b->items=0;
  b->head=0;
  b->tail=0;
  b->empty=1;
  b->full=0;
  b->mut = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t));
  pthread_mutex_init(b->mut,NULL);
  b->notFull = (pthread_cond_t*)malloc(sizeof(pthread_cond_t));
  pthread_cond_init(b->notFull,NULL); 
  b->notEmpty = (pthread_cond_t*)malloc(sizeof(pthread_cond_t));
  pthread_cond_init(b->notEmpty,NULL); 

  return b;
}

void bufferDelete(buffer *b){
  pthread_mutex_destroy (b->mut);
  free(b->mut);
  pthread_cond_destroy (b->notFull);
  free(b->notFull); 
  pthread_cond_destroy (b->notEmpty);
  free(b->notEmpty);
  free(b->string);
  free(b);
}

void bufferRem(buffer *b){
  b->items--;          // decrease length of buffer
  b->head++;           // May be considered bad practice... but don't actually delete just move
  if(b->head==b->max){ // Make it a circular buffer
    b->head=0;
  }
  if(b->tail==b->head){ // Head met tail, we are empty
    printf("Line: %d Buffer is empty.\n",__LINE__);
    b->empty=1;
  }
  b->full=0;            // We can't be full if we just removed
return;
}

void bufferAdd(buffer *b,char *element){
  b->string[b->tail]=element; // Add string pointer to buffer - I was adding to head changed to tail
  b->items++;                 // buffer length +1
  b->tail++;                  // Move tail location +1
  if(b->tail==b->max){        // Make sure to have circular buffer
    b->tail=0;
  }
  if(b->tail==b->head){       // Check when full
    printf("Line: %d Buffer is full.\n",__LINE__);
    b->full=1;
  }
  b->empty=0;                 // Can't be empty if we just added
return;
}//End of buffer add

char *front(buffer *b){
  /* Make sure that the buffer isn't empty */
  if(b->items==0){
    printf("Line: %d Buffer is empty.\n",__LINE__);
    return NULL;
  }
  else{
    //printf("Made it this far\n"); // Fixed this bug... turns out it had nothing to do with this..
    return (b->string[b->head]); 
  }
}



/* Producer: */

void *producer(void *p){
  char buff[256];                      // Make a buffer to write things too...
  char servFile[256]="output/serviced.txt";
  char sBuff[256];
  threadData *pShared; 
  pShared = (threadData *)p;
  
  //printf("Line: %d full: %d, empty: %d\n",__LINE__,pShared->q->full,pShared->q->empty);

  FILE *fH = pShared->fHandles;        // Make a file handler for input files  

  if(fH){
    while(fgets(buff,256,fH)!=NULL){
      //printf("PID: %lu read: %s",pthread_self(),buff);
      // Now add to the buffer 
      //if(!(pShared->q->full)){
        printf("Line: %d Producer locking.\n",__LINE__);
        pthread_mutex_lock(pShared->b->mut);                      // Taking (trying) lock
        while(pShared->b->full){
          printf("Line: %d Producer waiting\n",__LINE__);        //pPID: %lu is waiting, buffer full.",__LINE__,pthread_self());
          pthread_cond_wait(pShared->b->notFull,pShared->b->mut);// Block on condition and release lock
        }

        bufferAdd(pShared->b,buff);                         // Add data to buffer
        pthread_mutex_unlock(pShared->b->mut);              // Unlock buffer
        pthread_cond_signal(pShared->b->notEmpty);          // Make sure to signal that consumer can do something
        printf("Line: %d Producer writing: %s",__LINE__,front(pShared->b));
      //}//End of if buffer is full
      //else{
      //  printf("Queue is full.\n");
      //}
    }//End while
  }//End if handle loaded correctly

  // Make sure to flip the 'I am done bit'
  pShared->serviced++;
  pShared->b->isComplete=1;
  printf("Line: %d isComplete: %d\n",__LINE__,pShared->b->isComplete);

  // Before Closing it checks if it has any other files to service:
  //
  // Now write to serviced.txt how many this pid serviced:
  //pthread_mutex_loc(pShared->threadLock); // Take lock for this serive file
  FILE *sH = fopen(servFile,"a");
  sprintf(sBuff,"%lu serviced %d files.\n",pthread_self(),pShared->serviced);
  fputs(sBuff,sH);
  fclose(sH);
  //pthread_mutex_unlock(pShared->threadLock);

  pthread_exit(NULL);
}// End producer


/* Consumer */

void *consumer(void *c){
  char ip_buff[256];
  char tmp[256];  
  threadData *pShared;
  pShared = (threadData *)c;

  //printf("cPID: %lu Look I am a consumer\n",pthread_self());
  
  FILE *fH = pShared->fHandles;
  // Make sure we loop til done
  while(1){ 
    printf("Line: %d Consumer Locking.\n",__LINE__);
    pthread_mutex_lock(pShared->b->mut);
    while(pShared->b->empty){
      if(pShared->b->isComplete){
        pthread_exit(NULL);
        //break;
      }
      //else{
        printf("Line: %d Consumer waiting.\n",__LINE__);
        pthread_cond_wait(pShared->b->notEmpty,pShared->b->mut);     // Block thread till notEmpty 
      //}
    }//Done waiting for work
    printf("Line: %d Consumer read: %s\n",__LINE__,front(pShared->b));
    //Write front to the file...
    // First loop up IP address:
    sprintf(tmp,"%s",front(pShared->b)); 
    //if(dnslookup(ip_buff,tmp,sizeof(tmp))==UTIL_FAILURE){
    //  sprintf(tmp,"%s,",front(pShared->b));
    //}
    //else{
    //  sprintf(tmp,"%s,ip_buff",front(pShared->b));
    //}
    fputs(front(pShared->b),fH);//tmp,fH);
    bufferRem(pShared->b);
    pthread_mutex_unlock(pShared->b->mut);      // Unlock
    pthread_cond_signal(pShared->b->notFull);   // Signal producer

  }//At this point isComplete=1

  
  pthread_exit(NULL);
}//End consumer


/* -----------------Main--------------------------------- */ 

int main(int argc,char *argv[]){
  clock_t t0,t1;
  t0=clock();
  char fileName[256]="input/names1.txt";
  char toWrite[256]="output/results.txt";
  char *files[argc];
  // Create array of filenames 
  //FILE *fName = (FILE *)malloc(sizeof(FILE*)*(argc-1));
  for(int i=0; i<(argc-1); i++){
    //fName[i]=fopen(argv[i+1],"r");
    files[i] = argv[i+1];
    printf("A filename: %s\n",argv[i+1]);
    printf("%s\n",files[i]);
  }

  //printf("args: %d\nfilename 1: %s\nfilename 2: %s\n",argc-1,&fName[0],&fName[1]);//,argv[1],argv[2]);
  int bufferSize = 30;
  FILE *fHandle,*f2Write;                        // Make a file handler for input files  
  fHandle = fopen(fileName,"r");  // Read the file from the location of fName pointer
  f2Write = fopen(toWrite,"w");

  pthread_t prod0;
  pthread_t cons0;


  // Create dataset for producer 
  buffer *b = bufferInit(bufferSize);
  threadData *p = threadDataInit(b,fHandle);
  threadData *c = threadDataInit(b,f2Write);
  printf("full: %d, empty: %d\n",p->b->full,p->b->empty);

  // Create pthread, check that it makes correctly 
  if(pthread_create(&prod0,NULL,producer,p)){
    fprintf(stderr,"Error making pthread pro\n");
    return 1;
  }
  // Create pthread consumer
  if(pthread_create(&cons0,NULL,consumer,c)){
    fprintf(stderr,"Error making pthread con\n");
    return 1;
  }

  // Wait for thread to complete correctly
  if(pthread_join(prod0,NULL)){
    fprintf(stderr,"Error joining prod.\n");
    return 2;
  }
  if(pthread_join(cons0,NULL)){
    fprintf(stderr,"Error joining cons.\n");
    return 2;
  }


  // Testing my producer */
  printf("Top: %s\n",front(p->b));
  //printf("isEmpty: %d, isFull: %d\n",q->empty,q->full);
  // Clean up 
  //bufferDelete(q);
  fclose(fHandle);
  fclose(f2Write);
  //for(int i=0; i<argc;i++){
  //  fclose(fName[i]);
  //}
  //free(fName);

  threadDataDelete(c);
  threadDataDelete(p);
  bufferDelete(b);

  // Finished and looking at timing
  t1=clock();
  printf("Finished in: %f.\n",(double)(t1-t0)/CLOCKS_PER_SEC);
  return 0;
}//End of main







