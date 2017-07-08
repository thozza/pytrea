# BSD 3-Clause License
#
# Copyright (c) 2017, Tomas Hozza
# All rights reserved.
#
# For full license, see LICENSE file

import pymodbus.constants

from pymodbus.client.sync import ModbusTcpClient

import logging
logger = logging.getLogger(__name__)


class AtreaUnitBase(object):
    pass


class AtreaUnitRD5(object):
    """
    Notes:
        - communication port is 503/TCP
        - address for modbus device over TCP/IP is irrelevant (any in 0-255)
        - when reading or writing multiple indexes in a single transaction, one has to make sure there is at least
        5 seconds delay between sessions.
    """

    def __init__(self, address, port=pymodbus.constants.Defaults.Port):
        self._address = address
        self._port = port
        self.client = ModbusTcpClient(self._address, self._port)
        self.client.connect()

    @staticmethod
    def _raw_temperature_value_to_float(value):
        """
        Map temperature values returned by Atrea units to float
        Values:
            65036 ~ -50,0 C .. 65535 ~ -0,1 C
            1 ~ 0,1 C .. 1300 ~ 130,0 C
        """
        if value > 1300:
            temperature = (65536 - value) * -0.1
        else:
            temperature = value * 0.1
        return temperature

    @staticmethod
    def _float_to_raw_temperature(value):
        """
        Map float temperature values values expected by Atrea units
        Values:
            65036 ~ -50,0 C .. 65535 ~ -0,1 C
            1 ~ 0,1 C .. 1300 ~ 130,0 C
        """
        if value < 0.0:
            raw_temperature = int(value * 10)

    def read_temperature_cp(self):
        """
        Input temperature from CP Touch controller.

        Register: I10207
        Values:
            65036 ~ -50,0 C .. 65535 ~ -0,1 C
            1 ~ 0,1 C .. 1300 ~ 130,0 C
        :return:
        """
        response = self.client.read_input_registers(10207)
        raw_temperature = response.getRegister(0)
        return self._raw_temperature_value_to_float(raw_temperature)

    def _read_data(self):
        pass

    def _write_data(self):
        pass

