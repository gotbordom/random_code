// Things that could go in a header:

/* Structs */
struct semaphore;
struct files2read;

/* Methods */
void *producers(); // What the producer threads will call
void *consumers(); // What the consumer threads will call
void wait(struct semaphore *S);
void signal(struct semaphore *S);
void init_semaphore(semaphore *S,int n,int buffer);
void dest_semaphore(semaphore *S);

