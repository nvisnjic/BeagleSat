/**
 * @file   inoutlkm.c
 * @author Niko Visnjc
 * @date   20 July 2015
 * @version 0.1
 * @brief   A most basic input output Linux loadable kernel module (LKM) using  * sysfs devices
 * Based on the LKM programming write-up from http://www.derekmolloy.ie/
 * @see ...
 */



#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/gpio.h>       // Required for the GPIO functions
#include <linux/interrupt.h>  // Required for the IRQ code
#include <linux/kobject.h>    // Using kobjects for the sysfs bindings
#include <linux/time.h>       // Using the clock to measure time between button presses

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Niko Visnjic");
MODULE_DESCRIPTION("Basic input -> output kernel module");
MODULE_VERSION("0.1");


static char   devName[10] = "inoutlkm";      ///< Null terminated default string -- just in case

//static int    inputData = 0;            ///< For information, store the number of button presses
//static int   outputData = 0;                    ///< Is the LED on or off? Used to invert its state (off by default)


static int X_in = 0;
static int Y_in = 0;
static int Z_in = 0;

/** @brief A callback function to output the inputData variable
 *  @param kobj represents a kernel object device that appears in the sysfs filesystem
 *  @param attr the pointer to the kobj_attribute struct
 *  @param buf the buffer to which to write the number of presses
 *  @return return the total number of characters written to the buffer (excluding null)
 */
static ssize_t inputData_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   //return sprintf(buf, "%d\n", inputData);
	
   return sprintf(buf, "X: %d Y: %d Z: %d\n", X_in, Y_in, Z_in);
}

/** @brief A callback function to read in the inputData variable
 *  @param kobj represents a kernel object device that appears in the sysfs filesystem
 *  @param attr the pointer to the kobj_attribute struct
 *  @param buf the buffer from which to read the number of presses (e.g., reset to 0).
 *  @param count the number characters in the buffer
 *  @return return should return the total number of characters used from the buffer
 */
static ssize_t inputData_store(struct kobject *kobj, struct kobj_attribute *attr,
                                   const char *buf, size_t count){
   sscanf(buf, "%d %d %d", &X_in, &Y_in, &Z_in);
   
   return count;
}

/** @brief Displays if the LED is on or off */
static ssize_t outputData_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf){
   //return sprintf(buf, "%d\n", outputData);

   return sprintf(buf, "X: %d Y: %d Z: %d \t (+1, -2, +6) \n", 
		X_in + 1, Y_in - 2, Z_in + 6);

}


/**  Use these helper macros to define the name and access levels of the kobj_attributes
 *  The kobj_attribute has an attribute attr (name and mode), show and store function pointers
 *  The count variable is associated with the numberPresses variable and it is to be exposed
 *  with mode 0666 using the numberPresses_show and numberPresses_store functions above
 */
static struct kobj_attribute input_attr = __ATTR(inputData, 0666, inputData_show, inputData_store);

/**  The __ATTR_RO macro defines a read-only attribute. There is no need to identify that the
 *  function is called _show, but it must be present. __ATTR_WO can be  used for a write-only
 *  attribute but only in Linux 3.11.x on.
 */
static struct kobj_attribute output_attr = __ATTR_RO(outputData);     ///< the ledon kobject attr

/**  The ebb_attrs[] is an array of attributes that is used to create the attribute group below.
 *  The attr property of the kobj_attribute is used to extract the attribute struct
 */
static struct attribute *inout_attrs[] = {
      &input_attr.attr,                  ///< The number of button presses
      &output_attr.attr,                  ///< Is the LED on or off?
      NULL,
};

/**  The attribute group uses the attribute array and a name, which is exposed on sysfs -- in this
 *  case it is gpio115, which is automatically defined in the ebbButton_init() function below
 *  using the custom kernel parameter that can be passed when the module is loaded.
 */
static struct attribute_group attr_group = {
      .name  = devName,                 ///< The name is generated in ebbButton_init()
      .attrs = inout_attrs,                ///< The attributes array defined just above
};

static struct kobject *ebb_kobj;

/** @brief The LKM initialization function
 *  The static keyword restricts the visibility of the function to within this C file. The __init
 *  macro means that for a built-in driver (not a LKM) the function is only used at initialization
 *  time and that it can be discarded and its memory freed up after that point. In this example this
 *  function sets up the GPIOs and the IRQ
 *  @return returns 0 if successful
 */
static int __init ebbButton_init(void){
   int result = 0;

   printk(KERN_INFO "inoutLKM: Initializing the basic input-output LKM\n");
   sprintf(devName, "inoutLKM");           // Create the gpio115 name for /sys/ebb/gpio115

   // create the kobject sysfs entry at /sys/ebb -- probably not an ideal location!
   ebb_kobj = kobject_create_and_add("inout", kernel_kobj->parent); // kernel_kobj points to /sys/kernel
   if(!ebb_kobj){
      printk(KERN_ALERT "EBB Button: failed to create kobject mapping\n");
      return -ENOMEM;
   }
   // add the attributes to /sys/ebb/ -- for example, /sys/ebb/gpio115/numberPresses
   result = sysfs_create_group(ebb_kobj, &attr_group);
   if(result) {
      printk(KERN_ALERT "EBB Button: failed to create sysfs group\n");
      kobject_put(ebb_kobj);                          // clean up -- remove the kobject sysfs entry
      return result;
   }

   return result;
}

/** @brief The LKM cleanup function
 *  Similar to the initialization function, it is static. The __exit macro notifies that if this
 *  code is used for a built-in driver (not a LKM) that this function is not required.
 */
static void __exit ebbButton_exit(void){
//   printk(KERN_INFO "EBB Button: The button was pressed %d times\n", numberPresses);
   kobject_put(ebb_kobj);                   // clean up -- remove the kobject sysfs entry
   
   printk(KERN_INFO "inoutLKM: Goodbye from the basic input-output LKM!\n");
}


// This next calls are  mandatory -- they identify the initialization function
// and the cleanup function (as above).
module_init(ebbButton_init);
module_exit(ebbButton_exit);
