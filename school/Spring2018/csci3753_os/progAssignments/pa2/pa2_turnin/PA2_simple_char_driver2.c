

#include<linux/init.h>
#include<linux/module.h>
#include<linux/kernel.h>
#include<linux/fs.h>
#include<linux/slab.h>
#include<linux/uaccess.h>
#include<asm/uaccess.h>

#define BUFFER_SIZE 1024

/* Define device_buffer and other global data structures you will need here */
#define DEVICE_NAME "PA2_simple_char_driver"
//#define CLASS_NAME "simple_char"

// Adding modinfo ...
MODULE_LICENSE("GPL");  // Not sure I reallllly need this for class but hey why not.
MODULE_AUTHOR("Anthony Tracy");
MODULE_DESCRIPTION("OS PA2 simple charecter driver for my linux popcorn kernel");
MODULE_VERSION("0.1");

// Things I may need not really sure...
static int   majorNum;  // Given what I made this should become 621 ... 
static char  *msg;      // Makeing it dynamic...// This is for storing the message being passed - I need to make this dynamic....
//static short som;     // This is for knowing length of message passed
//static short pos;
static int   nOpen;     // A counter for how often the device is opened 
// pointers


// Method declarations....
static ssize_t simple_char_driver_read (struct file *, char __user *, size_t, loff_t *);
static ssize_t simple_char_driver_write (struct file *, const char __user *, size_t, loff_t *);
static int simple_char_driver_open (struct inode *, struct file *);
static int simple_char_driver_close (struct inode *, struct file *);
static loff_t simple_char_driver_seek (struct file *, loff_t, int);



ssize_t simple_char_driver_read (struct file *pfile, char __user *buffer, size_t length, loff_t *offset)
{
	/* *buffer is the userspace buffer to where you are writing the data you want to be read from the device file*/
	/* length is the length of the userspace buffer*/
	/* offset will be set to current position of the opened file after read*/
	/* copy_to_user function: source is device_buffer and destination is the userspace buffer *buffer */

        // Update kernel log:
        //printk("PA2_simple_char_driver: Read file at offset: %i, reading byte count: %u",(int)*offset,(unsigned int) length);
        // Make usful variables:
        int maxStr;
        int toRead;
        int read;
        
        maxStr = BUFFER_SIZE - *offset;     // If I start reading at offset there are only so many chars left

        // If I am trying to read paste the end of the file:
        if( maxStr > length ){
          toRead = length;
        }
        else{
          toRead = maxStr;
        }
        if(toRead ==0){printk(KERN_INFO "PA2_simple_char_device: End of device.\n");}
        // send bytes to user's buffer:
        read = toRead-copy_to_user(buffer,msg + *offset,toRead);

        // If I am trying to read more than the data available then only read the available:
        //if( *offset+length > som) {length = som - *offset;}
        // Watch for errors:
        //if(copy_to_user(buffer,msg + *offset,length) != 0) {return -EFAULT;}
        // increment the position in file: - what I was forgetting initially....
        *offset += read;
        printk("PA2_simple_char_driver: Read file at offset: %i, reading byte count: %u",(int)*offset,(unsigned int) read);
        return read;  
  
}



ssize_t simple_char_driver_write (struct file *pfile, const char __user *buffer, size_t length, loff_t *offset)
{
	/* *buffer is the userspace buffer where you are writing the data you want to be written in the device file*/
	/* length is the length of the userspace buffer*/
	/* current position of the opened file*/
	/* copy_from_user function: destination is device_buffer and source is the userspace buffer *buffer */
        // sprintf(where to put string, format of string, args for string, 
        //sprintf(msg,"%s(%zu chars)",buffer,length); // Probably the only line that the Captain isn't a part of.. not anymore...
        //som = strlen(msg);                          
        
        // Using similar vars as read:
        int maxStr;
        int toWrite;
        int written;
        
        maxStr = BUFFER_SIZE - *offset;
        // Set length of toWrite based on length and buffer:
        if(maxStr>length){
          toWrite=length;
        }
        else{
          toWrite=maxStr;
        }

        written = toWrite - copy_from_user(msg + *offset,buffer, toWrite);
        printk(KERN_INFO "PA2_simple_char_driver: Written %i charecters\n", (unsigned int) written);
        
        *offset += written;
	return written;
}


int simple_char_driver_open (struct inode *pinode, struct file *pfile)
{
	/* print to the log file that the device is opened and also print the number of times this device has been opened until now*/
        nOpen++;
        printk(KERN_INFO "PA2_simple_char_driver: Device opened %d time(s)\n",nOpen);
	return 0;
}

int simple_char_driver_close (struct inode *pinode, struct file *pfile)
{
	/* print to the log file that the device is closed and also print the number of times this device has been closed until now*/
	printk(KERN_INFO "PA2_simple_char_driver: Closing device. Had been opened %d time(s)\n",nOpen);
	return 0;
}

loff_t simple_char_driver_seek (struct file *pfile, loff_t offset, int whence)
{
	/* Update open file position according to the values of offset and whence */
        // Look at the current pos we are at in the opened file system....
        // Make position pointer:
        loff_t pos = 0;
        switch(whence){
          case 0 :
            pos = offset;
            break;
          case 1 :
            pos = pfile->f_pos + offset;
            break;
          case 2 :
            pos = BUFFER_SIZE - offset;
            break;
        }
        // move current pointer to f_pos  <- current location
        pfile->f_pos = pos;
 
        //if(whence == 0) {pfile = offset;}
        //if(whence == 1) {pfile += offset;}
        //if(whence == 2) {pfile = som-offset;}
        // In all of these cases check if new *pfile is within the *startFile and *endFile else: return error and don't change position...
	return pos;
}

struct file_operations simple_char_driver_file_operations = {

	.owner   = THIS_MODULE,
	.open    = simple_char_driver_open,
        .read    = simple_char_driver_read,
        .write   = simple_char_driver_write,
        .release = simple_char_driver_close,
        .llseek  = simple_char_driver_seek,
	/* add the function pointers to point to the corresponding file operations. look at the file fs.h in the linux souce code*/
};

static int __init simple_char_driver_init(void)
{
	/* print to the log file that the init function is called.*/
        printk(KERN_INFO "PA2_simple_char_driver: The driver is initiated.\n");
	/* register the device */
        // I guess if I just use 0 it should allocate a device driver for me? That seems cool, but for now... I think I'll just stick to making one... SHAZAM! make me a driver..
        majorNum = register_chrdev(262,DEVICE_NAME,&simple_char_driver_file_operations); // So using 0 and auto building driver... not best using 261
        if(majorNum < 0){
          printk(KERN_ALERT "PA2_simple_char_driver: Failed to register a major number\n");
          return majorNum;
        }
	printk(KERN_INFO "PA2_simple_char_driver: Registered with the major number %d\n", majorNum);
        // Add buffer: - now that I have made it dynamic:
        msg = kmalloc(BUFFER_SIZE,GFP_KERNEL);
        // fill dataset:
        memset(msg,'\0',8*sizeof(char)); // I've seen this done a few ways, not really sure I even need it but ... sure
        return 0;
}

static void __exit simple_char_driver_exit(void)
{
	/* print to the log file that the exit function is called.*/
        printk(KERN_INFO "PA2_simple_char_driver: Driver has been stopped.\n");
	/* unregister  the device using the register_chrdev() function. */
        unregister_chrdev(majorNum,DEVICE_NAME);
        // Deallocate mem:
        kfree(msg);
}

/* add module_init and module_exit to point to the corresponding init and exit function*/
module_init(simple_char_driver_init);
module_exit(simple_char_driver_exit);
