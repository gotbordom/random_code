#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>
#include<errno.h>   // Error handeling


// Currnetly working with non-dynamic buffer:
#define BUFFER_LENGTH 1056

//static char received[BUFFER_LENGTH];


int main(){
  // Initilize variables:
  int toLKM,fromLKM,file,bytes2read,seeker;
  char string2file[BUFFER_LENGTH];
  char line[50];
  int option; // Should either be 'r','w','s', or 'e'
  int whence,offset;
  // Begin test:
  printf("Starting test:\n");
  // Opent eh device file:
  file = open("/dev/PA2_simple_character_device2",O_RDWR);

  // watching for possible erros...
  if(file<0){
    perror("Failed to open Driver file.");
    return errno;
  }

  
  do{
    printf("Press 1 to read from device\n");
    printf("Press 2 to write to device\n");
    printf("Press 3 to seek into device\n");
    printf("Press 4 to exit from device\n");
    //fgets (line, sizeof(line), stdin);
    //sscanf(line,"%d",&option);
    printf("Enter choice: ");
    scanf("%d",&option);
    // Start menu options;
    switch (option){
      case 1: { // Read to device
        //printf("Case1: I typed in: %d\n",option);
        printf("Enter number of bytes to read: ");
        //getchar();
        scanf("%d",&bytes2read);
        char *received = malloc(bytes2read);
        fromLKM=read(file,received,bytes2read);
        if(fromLKM<0){
          perror("Failed to read.");
          return errno;
        }
        printf("Received message:\n");
        printf("%s",received);
        printf("\n");
      }
      break;
      case 2: { // Write to device
        //printf("Case2: I typed in: %d\n",option); 
        printf("Enter string to write to kernel: ");
        scanf("%1023s",string2file);  // This is cool so it will take the whole string till 
                                         // a new line is entered, then leave out the newline..
        printf("Message being written to device is:\n%s\n",string2file);
        toLKM = write(file,string2file,strlen(string2file));  // Actually send file

        if(toLKM<0){
          perror("Failed to write to device.");
          return errno;
        }
      }
      break;
      case 3: {// scan device
        printf("Choose offset: ");
        scanf("%d",&offset);
        printf("Choose whence value: ");
        scanf("%d",&whence);
      }
      break;
      case 4:{ 
        printf("Closing\n");
      }
      break;
    }
  } while(option != 4);
  return 0;
}
