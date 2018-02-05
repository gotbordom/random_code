#include<stdio.h>
#include<linux/kernel.h>
#include<sys/syscall.h>
#include<unistd.h>
int main()
{

// Testing syscall for hello world!...
long int amma = syscall(333);
printf("System call sys_helloworld returned %ld\n",amma);


// testing syscall for simple_addk
// So my code uses call by referencing... pasically I pass the pointer into the function:

// make a value for the sum to use, give it 0... sure why not.
int simple_sum=0;
int a=10;
int b=20;

long int test_add = syscall(334,a,b,&simple_sum);
printf("System call sys_simple_add returned %ld\n",test_add);
printf("Check log with dmesg to verify sum: %d, and the address is: %p\n",simple_sum,&simple_sum);
}

