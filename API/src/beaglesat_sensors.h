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
};

/**
 * @brief Coordinate triplet structure
 * Structure containing X, Y & Z measurement data
 */
typedef struct XYZdata {
    float X; 
    float Y;
    float Z;
};




/**
*
* @brief Initialization for BeagleSat struct
* @todo add parsing from config file 
*/
void BeagleSat_init(struct BeagleSat *sat, char *config_path) {
    
}

/**
*
* @brief Get unprocessed data from sensor
* @todo sensorID should be an enum (probably?) to avoid confusion with
* numerical ID memorization. 
* @todo Is it a good idea to return the triplet? 
* probably not, but it's useful from a usability perspective, maybe, 
* returning int would be better for error checking though.
*/
struct XYZdata BeagleSat_getRawData(struct BeagleSat *sat, int sensorID) {
    
    char *devicePointer = sat->sensorList[sensorID]->device;
    /* Read from sysfs device driver and get triplet*/
    // struct XYZdata dataRead =  
    
    return XYZdata
}

/**
 * @brief Example showing how to document a function with Doxygen.
 * @warning Warning.
 */
struct XYZdata BeagleSat_getCorrectedData(struct BeagleSat *sat, int sensorID) {
     
    struct XYZdata dataIn = BeagleSat_getRawData(sat, sensorID);
    struct XYZdata correctedData;

    //* Invoke computation of Correction parameters, or load stored ones */
    struct params correctionParams =
            BeagleSat_computeParameters(sat, SensorID); 
            // this is tricky, since there are a huge number of options
            // lets say, we have smart defaults for now...
             

/// @todo filter enabled flag; keep/drop?
    if (sat->sensor[sensorID]->filter_enabled) { 
        correctedData = BeagleSat_correctData(dataIn, correctionParams);
    }
    else {
        correctedData = dataIn;
    }

    return XYZdata;
}

#endif /* _BEAGLESAT_SENSORS_H_ */
