/*************************************************************************
 * Copyright (C) 2015 Niko Visnjic                                       *
 *                                                                       *
 * This file is part of BeagleSat.                                       *
 *                                                                       *
 * Should add a description and some licence stuff here later.           *
 *                                                                       *
 *************************************************************************/

/**
 * @file beaglesat_sensors.h
 * @brief Beaglesat sensor module API header
 *
 * Long text at some point.
 *
 * @see http://github.com/nvisnjic/beaglesat/
 */

#ifndef _BEAGLESAT_SENSORS_H_
#define _BEAGLESAT_SENSORS_H_

#include <time.h>


typdef float IGRF;

/**
 * @brief Sensor structure
 * Sensor structure for data on specific devices used
 */
typedef struct Sensor {
    int ID;             /**< Numerical sensor identificator             */
    char *device;       /**< sensor sysfs device (change to pointer?)   */
    int paramNumber;    /**< number of correction parameters            */
    double *params;     /**< array of correction parameters             */
    time_t lastFitting: /**< time of last correction parameter update   */
};


/**
 * @brief BeagleSat structure
 * Structure containing all data needed for a BeagleSat system
 */
typedef struct BeagleSat {
    IGRF currentIGRF;   /**< Set geomagnetic reference value            */
    sensor *sensorList; /**< list of all registered sensor devices      */ 
    //telemetry, comms, other stuff..
}


/**
*
* @brief Initialization for BeagleSat struct
* @todo add parsing from config file 
*/
void BeagleSat_init(struct BeagleSat *sat, char *config_path) {
    
}

void BeagleSat_getRawVelocity(struct BeagleSat *sat, float *x, float *y, float *z) {
    *x = 1;
    *y = 1;
    *z = 1;
}

/**
 * @brief Example showing how to document a function with Doxygen.
 * @warning Warning.
 */
int BeagleSat_getVelocity(struct BeagleSat *sat, float *x, float *y, float *z) {
    float x_raw, y_raw, z_raw;
    BeagleSat_getRawVelocity(sat, &x_raw, &y_raw, &z_raw);

    if (sat->filter_enabled) {
        BeagleSat_filterVelocity(&x_raw, &y_raw, &z_raw);
    }
    else {
        *x = x_raw;
        *y = y_raw;
        *z = z_raw
    }
    return 1;
}

#endif /* _BEAGLESAT_SENSORS_H_ */
