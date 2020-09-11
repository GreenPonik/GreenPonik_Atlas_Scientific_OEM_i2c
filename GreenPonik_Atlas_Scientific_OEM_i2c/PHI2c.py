#! /usr/bin/python3

"""
@package Class to communicate with Atlas Scientific sensors in I2C mode.
###########################################################################
###########################################################################
###########################################################################
####################### Atlas Scientific i2c ##############################
########################### by GreenPonik #################################
###########################################################################
###########################################################################
###########################################################################
Source code is based on Atlas Scientific documentations:
https://www.atlas-scientific.com/files/EC_oem_datasheet.pdf
https://atlas-scientific.com/files/oem_pH_datasheet.pdf
"""
from GreenPonik_Atlas_Scientific_OEM_i2c.CommonsI2c import _CommonsI2c


class PHI2c(_CommonsI2c):
    """
    @brief specific methods for OEM PH module
    """

    # ----- Getters pH methods ----- ######

    def get_slope_probe(self):
        """
        @brief Get the pH probe slope
        """
        raise NotImplementedError('not implemented yet')

    # ----- Setters pH methods ----- ######
