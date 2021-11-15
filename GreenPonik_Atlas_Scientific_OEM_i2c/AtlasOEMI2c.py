#! /usr/bin/python3

"""
Description
------------
Class to communicate with Atlas Scientific OEM sensors in I2C mode.
Atlas Scientific i2c by GreenPonik
Source code is based on Atlas Scientific documentations:

https://www.atlas-scientific.com/files/EC_oem_datasheet.pdf

https://atlas-scientific.com/files/oem_pH_datasheet.pdf
"""
import time
from adafruit_extended_bus import ExtendedI2C as I2C
from Adafruit_PureIO.smbus import SMBus


class _AtlasOEMI2c:
    # TODO add compatibility to use it with the with statement
    ALLOWED_MODULES_TYPES = {
        "EC",
        "PH",
    }
    ADDR_OEM_HEXA = {
        0x64,  # EC
        0x65,  # PH
        0x66,  # ORP
        0x67,  # DO
    }
    """
    Array key=>value for each OEM sensors i2c hexa addresses
    """
    ADDR_OEM_DECIMAL = {
        100,  # EC
        101,  # PH
        102,  # ORP
        103,  # DO
    }
    """
    Array value of each OEM sensors decimal addresses
    """
    ADDR_OEM_TXT_TO_HEXA = {
        "EC": 0x64,
        "PH": 0x65,
        "ORP": 0x66,
        "DO": 0x67,
    }
    """
    Array key=>value for each OEM sensors name i2c hexa addresses
    """
    ADDR_OEM_HEXA_TO_DECIMAL = {
        0x64: 100,  # DO
        0x65: 101,  # ORP
        0x66: 102,  # PH
        0x67: 103,  # EC
    }
    """
    Array key=>value for each OEM sensors i2c hexa to decimal addresses
    """

    OEM_EC_REGISTERS = {
        "device_type": 0x00,
        "device_firmware": 0x01,
        "device_addr_lock": 0x02,
        "device_addr": 0x03,
        "device_intr": 0x04,
        "device_led": 0x05,
        "device_sleep": 0x06,
        "device_new_reading": 0x07,
        "device_probe_type_msb": 0x08,  # 0x08 - 0x09 2 registers
        "device_probe_type_lsb": 0x09,  # 0x08 - 0x09 2 registers
        "device_calibration_msb": 0x0A,  # 0x0A - 0x0D 4 registers
        "device_calibration_high": 0x0B,  # 0x0A - 0x0D 4 registers
        "device_calibration_low": 0x0C,  # 0x0A - 0x0D 4 registers
        "device_calibration_lsb": 0x0D,  # 0x0A - 0x0D 4 registers
        "device_calibration_request": 0x0E,
        "device_calibration_confirm": 0x0F,
        "device_temperature_comp_msb": 0x10,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_high": 0x11,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_low": 0x12,  # 0x10 - 0x13 4 registers
        "device_temperature_comp_lsb": 0x13,  # 0x10 - 0x13 4 registers
        "device_temperature_confirm_msb": 0x14,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_high": 0x15,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_low": 0x16,  # 0x14 - 0x17 4 registers
        "device_temperature_confirm_lsb": 0x17,  # 0x14 - 0x17 4 registers
        "device_ec_msb": 0x18,  # 0x18 - 0x1B 4 registers
        "device_ec_high": 0x19,  # 0x18 - 0x1B 4 registers
        "device_ec_low": 0x20,  # 0x18 - 0x1B 4 registers
        "device_ec_lsb": 0x21,  # 0x18 - 0x1B 4 registers
        "device_tds_msb": 0x1C,  # 0x1C - 0x1F 3 registers
        "device_tds_high": 0x1D,  # 0x1C - 0x1F 3 registers
        "device_tds_low": 0x1E,  # 0x1C - 0x1F 3 registers
        "device_tds_lsb": 0x1F,  # 0x1C - 0x1F 3 registers
        "device_salinity_msb": 0x20,  # 0x20 - 0x23 4 registers
        "device_salinity_high": 0x21,  # 0x20 - 0x23 4 registers
        "device_salinity_low": 0x22,  # 0x20 - 0x23 4 registers
        "device_salinity_lsb": 0x23,  # 0x20 - 0x23 4 registers
    }

    OEM_PH_REGISTERS = {
        "device_type": 0x00,
        "device_firmware": 0x01,
        "device_addr_lock": 0x02,
        "device_addr": 0x03,
        "device_intr": 0x04,
        "device_led": 0x05,
        "device_sleep": 0x06,
        "device_new_reading": 0x07,
        "device_calibration_msb": 0x08,  # 0x08 - 0x0B 4 registers
        "device_calibration_high": 0x09,  # 0x08 - 0x0B 4 registers
        "device_calibration_low": 0x0A,  # 0x08 - 0x0B 4 registers
        "device_calibration_lsb": 0x0B,  # 0x08 - 0x0B 4 registers
        "device_calibration_request": 0x0C,
        "device_calibration_confirm": 0x0D,
        "device_temperature_comp_msb": 0x0E,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_high": 0x0F,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_low": 0x10,  # 0x0E - 0x11 4 registers
        "device_temperature_comp_lsb": 0x11,  # 0x0E - 0x11 4 registers
        "device_temperature_confirm_msb": 0x12,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_high": 0x13,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_low": 0x14,  # 0x12 - 0x15 4 registers
        "device_temperature_confirm_lsb": 0x15,  # 0x12 - 0x15 4 registers
        "device_ph_msb": 0x16,  # 0x16 - 0x19 4 registers
        "device_ph_high": 0x17,  # 0x16 - 0x19 4 registers
        "device_ph_low": 0x18,  # 0x16 - 0x19 4 registers
        "device_ph_lsb": 0x19,  # 0x16 - 0x19 4 registers
    }

    ONE_BYTE_READ = 0x01
    TWO_BYTE_READ = 0x02
    THREE_BYTE_READ = 0x03
    FOUR_BYTE_READ = 0x04

    # the default bus for I2C on the newer Raspberry Pis,
    # certain older boards use bus 0
    DEFAULT_BUS = 1

    # the timeout needed to query readings and calibrations
    DEFAULT_LONG_TIMEOUT = 1.5
    # timeout for regular commands
    DEFAULT_SHORT_TIMEOUT = 0.3

    EC_BINARY_CALIB_STATUS = {
        0: "nothing",
        1: "only dry",
        2: "only single",
        3: "dry and single",
        4: "only low",
        5: "dry and low",
        6: "single and low",
        7: "dry, single and low",
        8: "only high",
        9: "dry and high",
        10: "single and high",
        11: "dry, single and high",
        12: "low and high",
        13: "dry, low and high",
        14: "single, low and high",
        15: "all",
    }

    PH_BINARY_CALIB_STATUS = {
        0: "nothing",
        1: "only low",
        2: "only mid",
        3: "low and mid",
        4: "only high",
        5: "low and high",
        6: "mid and high",
        7: "all",
    }

    @property
    def debug(self):
        """debug property

        :getter: debug flag
        :setter: change debug flag

        Returns:
            bool: `True` if the debug mode is ON, `False` if not
        """
        return self._debug

    @debug.setter
    def debug(self, d: bool) -> None:
        """setter debug flag

        Args:
            d (bool): `True` to set debug mode ON, `False` to set debug mode OFF
        """
        self._debug = d

    @property
    def bus_number(self):
        """bus_number property

        :return: the i2c bus number
        :rtype: int
        """
        return self._bus_number

    @bus_number.setter
    def bus_number(self, bus_number: int) -> None:
        """bus_number property

        :param bus_number: the i2c bus number
        :type bus_number: int
        """
        self._bus_number = bus_number

    @property
    def address(self):
        """getter i2c address of the device

        :return: i2c address of the device on the i2c bus
        :rtype: int
        """
        return self._address

    @address.setter
    def address(self, address: int) -> None:
        """setter i2c address of the device

        :param address: i2c address of the device on the i2c bus
        :type address: int
        """
        self._address = address

    @property
    def short_timeout(self):
        """short delay to wait

        :return: short delay in milliseconds
        :rtype: int
        """
        return self._short_timeout

    @short_timeout.setter
    def short_timeout(self, timeout: int) -> None:
        """short delay to wait

        :param timeout: short delay in milliseconds
        :type timeout: int
        """
        self._short_timeout = timeout

    @property
    def long_timeout(self):
        """long delay to wait

        :return: long delay in milliseconds
        :rtype: int
        """
        return self._long_timeout

    @long_timeout.setter
    def long_timeout(self, timeout: int) -> None:
        """long delay to wait

        :param timeout: long delay in milliseconds
        :type timeout: int
        """
        self._long_timeout = timeout

    @property
    def name(self):
        """name of OEM circuit

        :return: name of OEM circuit
        :rtype: string
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """name of OEM circuit

        :param name: name of OEM circuit
        :type name: string
        """
        self._name = name

    @property
    def moduletype(self):
        """getter module type

        :return: get module type
        :rtype: string
        """
        return self._module

    @moduletype.setter
    def moduletype(self, m: str) -> None:
        """module type

        :param m: set the module type
        :type m: string
        """
        assert(m.upper() in ALLOWED_MODULES_TYPES)
        self._module = m.upper()

    def __init__(self, bus=DEFAULT_BUS, addr=None, moduletype=""):
        """create instance of AtlasI2c class
        :param bus: int => bus i2c bus number
        :param addr: int/hexa => device i2c address
        :param moduletype: string => device module type
        """
        if None is addr or (
            addr not in self.ADDR_OEM_HEXA and addr not in self.ADDR_OEM_DECIMAL
        ):
            raise Exception(
                "You have to give a value to addr argument \
                take a look on AtlasI2c.ADDR_OEM_HEXA \
                and AtlasI2c.ADDR_OEM_DECIMAL"
            )
        if moduletype not in self.ALLOWED_MODULES_TYPES:
            raise NotImplementedError(
                "sorry i can just interact \
                with EC or PH moduletype"
            )
        self._debug = False
        self._bus_number = bus
        self._address = addr
        self._name = moduletype.upper()
        self._module = moduletype.upper()
        self._short_timeout = self.DEFAULT_SHORT_TIMEOUT
        self._long_timeout = self.DEFAULT_LONG_TIMEOUT
        self._smbus = SMBus(self._bus_number)

    def read(self, register: int, num_of_bytes=1) -> bytes:
        """read data from i2c bus
        :param register > int i2c register to read
        :param num_of_byte > int number of bytes to read started from the register
        :return: raw value from i2c bus
        :rtype: bytes
        """
        if num_of_bytes > 1:
            raw = self._smbus.read_i2c_block_data(self._address, register, num_of_bytes)
        else:
            raw = self._smbus.read_byte_data(self._address, register)

        if self._debug:
            print("Read: %s registers start from: %s" % (num_of_bytes, hex(register)))
            print("Raw response from i2c: ", raw)
        return raw

    def write(self, register: int, v):
        """write data through i2c bus
        :param register > int i2c register to read
        :param v > int/bytearray to write through i2c
        """
        if (
            "int" != type(v).__name__
            and len(v) > 1
            and ("bytearray" == type(v).__name__ or "bytes" == type(v).__name__)
        ):
            self._smbus.write_i2c_block_data(self._address, register, v)
        elif "int" == type(v).__name__:
            self._smbus.write_byte_data(self._address, register, v)
        else:
            raise IOError("cannot write this in smbus/i2c: ", v)
        if self._debug:
            print("Write %s on register: %s" % (v, hex(register)))

    def list_i2c_devices(self) -> list:
        """save the current address so we can restore it after
        :return: list àf i2c addresses on the bus
        :rtype: list
        """
        with I2C(self._bus_number) as i2c:
            scan = i2c.scan()
            if self._debug:
                print("I2c devices found: ", scan)
            return scan

    def print_all_registers_values(self):
        """Print all register values
        """
        if "EC" == self._module:
            registers = self.OEM_EC_REGISTERS
        elif "PH" == self._module:
            registers = self.OEM_PH_REGISTERS
        for reg in range(0, len(registers)):
            print("Register: %s, Value: %s" % (hex(reg), self.read(reg)))
