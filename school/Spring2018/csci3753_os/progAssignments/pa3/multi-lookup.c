#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>

//MODULE_LICENSE("GPL");  // Not sure I reallllly need this for class but hey why not.
//MODULE_AUTHOR("Anthony Tracy");
//MODULE_DESCRIPTION("OS PA3: writing a script to create threads and loopup ip addresses");
//MODULE_VERSION("0.1");

/* Added the below stuff to a  header.. */


//void *producers(void *args); // What the producer threads will call
//void *consumers(); // What the consumer threads will call
/* ------------Struct Methods --------------- */
/* Semaphores */


//void wait(struct semaphore *S);
//void signal(struct semaphore *S);
//void init_semaphore(semaphore *S,int n,int buffer);
//void dest_semaphore(semaphore *S)
/* Queues */
//queue *queueInit(int size);
//void queueDelete(queue *q);
//void enqueue(queue *q, int in);
//void dequeue(queue *q, int out);
/* ThreadPools */
//pool_t *pool_init(void);
//void pool_del(pool_t *p);
//void enpool(pool_t *p);
//void depool(pool_t *p);



/* ------------Data structs------------------ */

typedef struct{
  int max,items;
  int head, tail;       // Need these locations
  int full, empty;      // want to know for signaling
  pthread_mutex_t *mut; // Make sure to have a lock for accessing this queue
  pthread_cond_t *notFull, *notEmpty; // Make sure to have conditions to signal on
  char **string;
} queue;


typedef struct{
  queue *q;            // Also need to pass the shared q to all threads
  FILE *fHandles;      // pointer to a string - the filename to read
  int items;           // want the number of files to be read
  int *isComplete;     // Are the files done being read or not (1) true (0) false - bit map would save space...
} pData;


/* Queues */
pData *pDataInit(queue *q,int size,FILE *fHandle);
void pDataDelete(pData *p);

queue *queueInit(int size);
void queueDelete(queue *q);
void enqueue(queue *q, char *element);
void dequeue(queue *q);
char *front(queue *q);



/* ------------Methods----------------------- */

// pData methods:
pData *pDataInit(queue *q, int numFiles,FILE *fHandle){
  pData *p;
  p = (pData *)malloc(sizeof(pData));
  p->q = q;
  p->fHandles = fHandle;
  p->isComplete = (int *)malloc(sizeof(int)*numFiles);
  p->items=numFiles;
  return p;
}
void pDataDelete(pData *p){
 free(p->isComplete);
 free(p);
}

// queue methods:
queue *queueInit(int size){
  queue *q;
  q = (queue *)malloc(sizeof(queue));

  q->string = (char**)malloc(sizeof(char*)*size);
  q->max=size;
  q->items=0;
  q->head=0;
  q->tail=0;
  q->full=0;
  q->empty=1;
  q->mut = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t));
  q->notFull = (pthread_cond_t*)malloc(sizeof(pthread_cond_t));
  pthread_cond_init(q->notFull,NULL); 
  q->notEmpty = (pthread_cond_t*)malloc(sizeof(pthread_cond_t));
  pthread_cond_init(q->notEmpty,NULL); 

  return q;
}

void queueDelete(queue *q){
  pthread_mutex_destroy (q->mut);
  free(q->mut);
  pthread_cond_destroy (q->notFull);
  free(q->notFull); 
  pthread_cond_destroy (q->notEmpty);
  free(q->notEmpty);
  free(q->string);
  free(q);
}

void dequeue(queue *q){
  q->items--;          // decrease length of queue
  q->head++;           // May be considered bad practice... but don't actually delete just move
  if(q->head==q->max){ // Make it a circular queue
    q->head=0;
  }
  if(q->tail==q->head){ // Head met tail, we are empty
    printf("Queue is empty.\n");
    q->empty=1;
  }
  q->full=0;            // We can't be full if we just dequeued
return;
}

void enqueue(queue *q,char *element){
  q->string[q->head]=element; // Add string pointer to queue
  q->items++;                 // queue length +1
  q->tail++;                  // Move tail location +1
  if(q->tail==q->max){        // Make sure to have circular queue
    q->tail=0;
  }
  if(q->tail==q->head){       // Check when full
    printf("Queue is full.\n");
    q->full=1;
  }
  q->empty=0;                 // Can't be empty if we just added
return;
}//End of Enqueue

char *front(queue *q){
  /* Make sure that the queue isn't empty */
  if(q->items==0){
    printf("Queue is empty.\n");
    return NULL;
  }
  else{
    //printf("Made it this far\n"); // Fixed this bug... turns out it had nothing to do with this..
    return (q->string[q->head]); 
  }
}



/* Producer: */

void *producer(void *p){
  /* Testing with a string-filename */
  char buff[256];                                 // Make a buffer to write things too...
  pData *pShared;
  pShared = (pData *)p;
  FILE *fH = pShared->fHandles;                        // Make a file handler for input files  

  //fHandle = fopen(fName,"r");  // Read the file from the location of fName pointer
  if(fH){
    while(fgets(buff,256,fH)!=NULL){
      printf("PID: %lu read: %s\n",pthread_self(),buff);
      /* Now add to the queue */
      printf("isFull: %d\n",pShared->q->empty);
      if(!(pShared->q->full)){
        printf("Trying an Add.\n");
        enqueue(pShared->q,buff);
      }//End of if queue is full
      else{
        printf("Queue is full.\n");
      }
    }//End while
  }//End if handle loaded correctly
  return NULL;
}// End producer


/* Consumer */


/* -----------------Main--------------------------------- */ 

int main(int argc,char *argv[]){
 
  char fileName[256]="input/names1.txt";
  //char *files[argc]=argv;
  /* Create array of filenames */
  //char *fName = (char *)malloc(sizeof(char*)*(argc-1));
  //for(int i=0; i<argc; i++){
  //  fName[i]=&argv[i+1];
  //}

  //printf("args: %d\nfilename 1: %s\nfilename 2: %s\n",argc-1,&fName[0],&fName[1]);//,argv[1],argv[2]);
  int queueSize = 5;
  FILE *fHandle;                        // Make a file handler for input files  
  fHandle = fopen(fileName,"r");  // Read the file from the location of fName pointer

  pthread_t prod0;
  pthread_t cons0;


  /* Create dataset for producer */
  queue *q = queueInit(queueSize);
  pData *p = pDataInit(q,1,fHandle);
  

  printf("fName: %s\n",fileName);
  /* Create pthread, check that it makes correctly */
  if(pthread_create(&prod0,NULL,producer,&p)){
    fprintf(stderr,"Error making pthread\n");
    return 1;
  }
  /* Wait for thread to complete correctly*/
  if(pthread_join(prod0,NULL)){
    fprintf(stderr,"Error joining.\n");
    return 2;
  }
  
  /* Testing my producer */
  printf("Top: %s\n",front(p->q));

  /* Clean up */
  queueDelete(q);
  pDataDelete(p);
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
