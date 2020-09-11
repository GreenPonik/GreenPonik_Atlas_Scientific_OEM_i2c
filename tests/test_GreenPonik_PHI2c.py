import unittest
from unittest.mock import patch
import sys


class FNCTLMock():
    def __init__(self):
        pass

    def ioctl(self):
        pass


class SmbusMock:
    def __init__(self):
        pass


sys.modules["fcntl"] = FNCTLMock()
sys.modules["smbus"] = SmbusMock()


class Test_PHI2c(unittest.TestCase):
    @patch("GreenPonik_Atlas_Scientific_OEM_i2c.PHI2c.PHI2c")
    def test_get_device_info(self, Mock):
        ph_i2c = Mock()
        expected = "SUCCESS: EC, module type: 4 and firmware is: 5"
        ph_i2c.get_device_info.return_value = expected
        info = ph_i2c.get_device_info()
        self.assertIsNotNone(info)
        self.assertEqual(info, expected)

    @patch("GreenPonik_Atlas_Scientific_OEM_i2c.PHI2c.PHI2c")
    def test_get_type(self, Mock):
        ph_i2c = Mock()
        expected = 1
        ph_i2c.get_type.return_value = expected
        value = ph_i2c.get_type()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "int")
        self.assertEqual(value, expected)

    @patch("GreenPonik_Atlas_Scientific_OEM_i2c.PHI2c.PHI2c")
    def test_get_firmware(self, Mock):
        ph_i2c = Mock()
        expected = 5
        ph_i2c.get_firmware.return_value = expected
        value = ph_i2c.get_firmware()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "int")
        self.assertEqual(value, expected)

    @patch("GreenPonik_Atlas_Scientific_OEM_i2c.PHI2c.PHI2c")
    def test_get_read(self, Mock):
        ph_i2c = Mock()
        expected = 6.23
        ph_i2c.get_read.return_value = expected
        value = ph_i2c.get_read()
        self.assertIsNotNone(value)
        self.assertTrue(type(value).__name__, "float")
        self.assertEqual(value, expected)


if __name__ == '__main__':
    unittest.main()
