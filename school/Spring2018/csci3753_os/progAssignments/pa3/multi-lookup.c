#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>

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
  pthread_mutex_t *mut; // Make sure to have a lock for accessing this queue
  pthread_cond_t *notFull, *notEmpty; // Make sure to have conditions to signal on
  char **string;
} buffer;


typedef struct{
  buffer *b;            // Also need to pass the shared q to all threads
  FILE *fHandles;      // pointer to a string - the filename to read
  //int items;           // want the number of files to be read
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
  p->fHandles = fHandle;
  //p->isComplete = 0;
  //p->items=numFiles;
  return p;
}
void threadDataDelete(threadData *p){
 //queueDelete(p->q);
 //free(p->isComplete);
 free(p);
}

// queue methods:
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
  b->items--;          // decrease length of queue
  b->head++;           // May be considered bad practice... but don't actually delete just move
  if(b->head==b->max){ // Make it a circular queue
    b->head=0;
  }
  if(b->tail==b->head){ // Head met tail, we are empty
    printf("Line: %d Buffer is empty.\n",__LINE__);
    b->empty=1;
  }
  b->full=0;            // We can't be full if we just dequeued
return;
}

void bufferAdd(buffer *b,char *element){
  b->string[b->tail]=element; // Add string pointer to queue - I was adding to head changed to tail
  b->items++;                 // queue length +1
  b->tail++;                  // Move tail location +1
  if(b->tail==b->max){        // Make sure to have circular queue
    b->tail=0;
  }
  if(b->tail==b->head){       // Check when full
    printf("Line: %d Buffer is full.\n",__LINE__);
    b->full=1;
  }
  b->empty=0;                 // Can't be empty if we just added
return;
}//End of Enqueue

char *front(buffer *b){
  /* Make sure that the queue isn't empty */
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
  threadData *pShared; 
  pShared = (threadData *)p;
  
  //printf("Line: %d full: %d, empty: %d\n",__LINE__,pShared->q->full,pShared->q->empty);

  FILE *fH = pShared->fHandles;        // Make a file handler for input files  

  if(fH){
    while(fgets(buff,256,fH)!=NULL){
      //printf("PID: %lu read: %s",pthread_self(),buff);
      // Now add to the queue 
      //if(!(pShared->q->full)){
        printf("Line: %d Producer locking.\n",__LINE__);
        pthread_mutex_lock(pShared->b->mut);                // Adding lock
        while(pShared->b->full){
          printf("Line: %d Producer waiting\n",__LINE__);//pPID: %lu is waiting, buffer full.",__LINE__,pthread_self());
          pthread_cond_wait(pShared->b->notFull,pShared->b->mut);  // Block on condition and release lock
        }
        bufferAdd(pShared->b,buff);                // Add data to queue
        pthread_mutex_unlock(pShared->b->mut);              // Unlock queue
        pthread_cond_signal(pShared->b->notEmpty);        // Make sure to signal that consumer can do something
        printf("Line: %d Producer writing: %s",__LINE__,front(pShared->b));
      //}//End of if queue is full
      //else{
      //  printf("Queue is full.\n");
      //}
    }//End while
  }//End if handle loaded correctly

  // Make sure to flip the 'I am done bit'
  pShared->b->isComplete=1;
  printf("Line: %d isComplete: %d\n",__LINE__,pShared->b->isComplete);
  return NULL;
}// End producer


/* Consumer */

void *consumer(void *c){
  char buff[256];
  threadData *pShared;
  pShared = (threadData *)c;
  
  //printf("cPID: %lu Look I am a consumer\n",pthread_self());
  
  FILE *fH = pShared->fHandles;
  // Make sure we loop til done
  while(!pShared->b->isComplete){ 
    printf("Line: %d Consumer Locking.\n",__LINE__);
    pthread_mutex_lock(pShared->b->mut);
    while(pShared->b->empty){
      if(pShared->b->isComplete){
        break;
      }
      else{
        printf("Line: %d Consumer waiting.\n",__LINE__);
        pthread_cond_wait(pShared->b->notEmpty,pShared->b->mut);     // Block thread till notEmpty 
      }
    }//Done waiting for work
    printf("Line: %d Consumer read: %s\n",__LINE__,front(pShared->b));
    //Write front to the file...
    bufferRem(pShared->b);
    pthread_mutex_unlock(pShared->b->mut);      // Unlock
    pthread_cond_signal(pShared->b->notFull);   // Signal producer
  }//At this point isComplete=1

  
  return NULL;
}//End consumer


/* -----------------Main--------------------------------- */ 

int main(int argc,char *argv[]){
 
  char fileName[256]="input/names1.txt";
  char toWrite[256]="output/results.txt";
  //char *files[argc]=argv;
  // Create array of filenames 
  //char *fName = (char *)malloc(sizeof(char*)*(argc-1));
  //for(int i=0; i<argc; i++){
  //  fName[i]=&argv[i+1];
  //}

  //printf("args: %d\nfilename 1: %s\nfilename 2: %s\n",argc-1,&fName[0],&fName[1]);//,argv[1],argv[2]);
  int queueSize = 30;
  FILE *fHandle,*f2Write;                        // Make a file handler for input files  
  fHandle = fopen(fileName,"r");  // Read the file from the location of fName pointer
  f2Write = fopen(toWrite,"w");

  pthread_t prod0;
  pthread_t cons0;


  // Create dataset for producer 
  buffer *b = bufferInit(queueSize);
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
  //queueDelete(q);
  threadDataDelete(c);
  threadDataDelete(p);
  bufferDelete(b);
  return 0;
}//End of main








/* ------------Old code and notes--------------------------- */
/* ------------Main Funciton(Testing Queue)----------------- */
/*
int main(){//int argc,char argv[]){

  char buff[256];
  //char test[256];
  FILE *fHandle;
  size_t nread;

  // Testing my queue, should throw a lot of "Queue is full"...
  queue *q = queueInit(5);

  fHandle=fopen("input/names1.txt","r");
  if(fHandle) {
    //while((nread = fread(buff,1,sizeof buff,fHandle)) >0)
      //fwrite(buff,1,nread,stdout);
    while(fgets(buff,256,fHandle)!=NULL){
      printf("Items: %d \n",q->items);
      printf("%s",buff);
      if (!(q->full)){
        enqueue(q,buff);
      }
      else{
        //test=front(q);
        //fgets(test,256,front(q));
        printf("Look one from queue:\n");
        printf("front: %s\n",front(q));
        dequeue(q);
        enqueue(q,buff);
      }
    }
  }
  printf("head: %s\n",q->string[0]);
  fclose(fHandle);
  queueDelete(q);
}
*/
