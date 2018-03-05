#include<stdio.h>
#include<pthread.h>

MODULE_LICENSE("GPL");  // Not sure I reallllly need this for class but hey why not.
MODULE_AUTHOR("Anthony Tracy");
MODULE_DESCRIPTION("OS PA3: writing a script to create threads and loopup ip addresses");
MODULE_VERSION("0.1");

// Things that could go in a header:
void *producers(); // What the producer threads will call
void *consumers(); // What the consumer threads will call
void wait(struct semaphore *S);
void signal(struct semaphore *S);
void init_semaphore(semaphore *S,int n,int buffer);
void dest_semaphore(semaphore *S)




/*--------------------Structs begin---------------------*/

typedef struct {
  int value;
  struct process *list; // who is waiting to be woken 
}semaphore;

typedef struct {
  struct files *list;  // files that still need to be read (Make it a bitmap instead?)
}files2read;



/*--------------------Semaphore methods begin---------------------*/

// Defining methods for the semiphores .. wish we had classes:
void wait(semaphore *S){
  S->value--; // Need memory to store that someone is waiting:
  // Then check if the current process / thread can take work:
  if(S->value<0){
    // blocking process and adding it to memory
      // Requires appending a process... 
    block();
  }//end if
}//end sig

void signal(semaphore *S){
  S->value++;
  // Now if anyone is waiting wake them up:
  p = S->list[0];
  if(S-> <=0){
    // Requires removing a process - not sure how to do this.....
    wakeup(p);
  }//end if
}//end sig

void init_semaphore(semaphore *S,int ni,int buffer){
  S->value=n;
  // for testing:
  printf("semaphore has been made with value: %d \n",n);
  S->list=malloc(sizeof(struct process)*buffer)
}//end init


void dest_semaphore(semaphore *S){
  free(S->list);
}



/*---------------------Producer methods begin-------------------------*/

void *producer(){
  // stuff to do with producer
  printf("Look I'm a producer!\n")
  pthread_exit(0);
}



/*---------------------Consumer methods begin--------------------------*/


void *consumer(){
  // Stuff to do with consumer....
  printf("Look I'm a consumer!\n")
  pthread_exit(0);
}
  
/*----------------------Main process begins----------------------------*/
int main(argc,char *argv[]){
  /* Makeing just one producer and one consumer thread for now */
  pthread_t tid;
  pthread_attr_t attr; /* use default attrs */
  
  /* In here I need to create all my structs */

  /* actually make the producer thread */
  pthread_attr_init(&attr);
  pthread_create(%tid,&attr,producer,argv[1])
  
  /* create the consumer*/
  pthread_create(%tid,&attr,consumer)
  
  /* later the above should create a producer & consumer pool */
  
  
  
}

