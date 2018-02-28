#include<linux/kernel.h>
#include<linux/linkage.h>
asmlinkage long sys_simple_add(int a,int b,int *loc)
{
*loc = a+b;
printk(KERN_INFO "%d+%d=%d stored at %p\n",a,b,*loc,loc);
return 0;
}
