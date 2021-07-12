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


class ECI2c(_CommonsI2c):
    """
    @brief specific methods for OEM EC module
    """

    # ----- Getters EC methods ----- ######

    def get_k_probe(self):
        """
        @brief Get current ec probe k
        """
        raise NotImplementedError('not implemented yet')

    # ----- Setters EC methods ----- ######

    def set_k_probe(self, k):
        """
        @brief Set the ec probe k
        """
        # raise NotImplementedError('not implemented yet')
        register = self.OEM_EC_REGISTERS["device_probe_type_msb"]

        byte_array = int(k * 100).to_bytes(2, "big")
        self.write(register, byte_array)
        if self.debug:
            print("set probe k to: %.2f" % k)
            print(
                "sent converted k to bytes: " % byte_array,
            )
