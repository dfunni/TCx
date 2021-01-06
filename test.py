import logging
import time
import smbus2 as smbus
from devices.MCP342x import MCP342x
from devices.MCP3424 import MCP3424
from devices.MCP9800 import MCP9800
from devices import thermocouple as tc

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    logging.basicConfig(level='INFO')
    bus = smbus.SMBus(1) 
    amb = MCP9800(bus)
    tc0 = MCP3424(bus, chan=0, tc_type='k_type')
    tc1 = MCP3424(bus, chan=1, tc_type='k_type')
    #tc1 = MCP342x(bus, resolution=18, gain=8, channel=0)
    for i in range(5):
        t0 = time.time()
        amb.convert()
        tc0.convert()
        tc1.convert()
        time.sleep(0.250)
        temp_amb = amb.read()
        v0 = tc0.read()
        temp_tc0 = round(tc.v2c(v0, 'k_type', 'low') + temp_amb, 4)
        t1 = time.time()
        v1 = tc1.read()
        temp_tc1 = round(tc.v2c(v1, 'k_type', 'low') + temp_amb, 4)
        t2 = time.time()
        print(f'{temp_tc0},{temp_tc1},{temp_amb}, dt:{t1-t0},{t2-t1},{t2-t0}')
        time.sleep(1)

