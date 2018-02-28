

#include<linux/init.h>
#include<linux/module.h>

#include<linux/fs.h>
#include<linux/slab.h>
#include<asm/uaccess.h>

#define BUFFER_SIZE 1024

/* Define device_buffer and other global data structures you will need here */
#define DEVICE_NAME = "PA2_simple_char_driver"
#define CLASS_NAME = "simple_char"

// Adding modinfo ...
MODULE_LICENSE("GPL");  // Not sure I reallllly need this for class but hey why not.
MODULE_AUTHOR("Anthony Tracy");
MODULE_DESCRIPTION("OS PA2 simple charecter driver for my linux popcorn kernel");
MODULE_VERSION("0.1");

// Things I may need not really sure...
static int   majorNum;
static char  msg[256] = {0};  // This is for storing the message being passed
static short som;             // This is for knowing length of message passed - may not use all of msg... (size of message - som)
static int   nOpen;           // A counter for how often the device is opened - honestly saw this in a how to though I might like the idea...
// pointers
static struct class* simple_charClass = NULL;   // pointer to class
static struct device* simple_charDevice = NULL; // pointer to dirver

// Method declarations....
static ssize_t simple_char_driver_read (struct file *, char __user *, size_t, loff_t *)
static ssize_t simple_char_driver_write (struct file *, const char __user *, size_t, loff_t *)
static int simple_char_driver_open (struct inode *, struct file *)
static int simple_char_driver_close (struct inode *, struct file *)
static loff_t* simple_char_driver_seek (struct file *, loff_t, int)



ssize_t simple_char_driver_read (struct file *pfile, char __user *buffer, size_t length, loff_t *offset)
{
	/* *buffer is the userspace buffer to where you are writing the data you want to be read from the device file*/
	/* length is the length of the userspace buffer*/
	/* offset will be set to current position of the opened file after read*/
	/* copy_to_user function: source is device_buffer and destination is the userspace buffer *buffer */

	return 0;
}



ssize_t simple_char_driver_write (struct file *pfile, const char __user *buffer, size_t length, loff_t *offset)
{
	/* *buffer is the userspace buffer where you are writing the data you want to be written in the device file*/
	/* length is the length of the userspace buffer*/
	/* current position of the opened file*/
	/* copy_from_user function: destination is device_buffer and source is the userspace buffer *buffer */

	return length;
}


int simple_char_driver_open (struct inode *pinode, struct file *pfile)
{
	/* print to the log file that the device is opened and also print the number of times this device has been opened until now*/
	return 0;
}

int simple_char_driver_close (struct inode *pinode, struct file *pfile)
{
	/* print to the log file that the device is closed and also print the number of times this device has been closed until now*/
	return 0;
}

loff_t* simple_char_driver_seek (struct file *pfile, loff_t offset, int whence)
{
	/* Update open file position according to the values of offset and whence */
	return 0;
}

struct file_operations simple_char_driver_file_operations = {

	.owner = THIS_MODULE,
	.open  = simple_char_driver_open,
        .read  = simple_char_driver_read,
        .write = simple_char_driver_write,
        .close = simple_char_driver_close,
        .seek  = simple_char_driver_seek,
	/* add the function pointers to point to the corresponding file operations. look at the file fs.h in the linux souce code*/
};

static int simple_char_driver_init(void)
{
	/* print to the log file that the init function is called.*/
        printk(KERN_INFO "simple_char_driver: The driver is initiated, Captain Marvel we need you!")
	/* register the device */
	return 0;
}

static void simple_char_driver_exit(void)
{
	/* print to the log file that the exit function is called.*/
        printk(KERN_INFO "simple_char_driver: Shazam! Captain Marvel is here! The Evil driver has been stopped")
	/* unregister  the device using the register_chrdev() function. */
}

/* add module_init and module_exit to point to the corresponding init and exit function*/
module_init(simple_char_driver_init);
module_exit(simple_char_driver_exit);
