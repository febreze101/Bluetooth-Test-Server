from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags

from bluez_peripheral.gatt.service import ServiceCollection
from ble.util import *

# Define a service
class YeastObserver(Service):
    def __init__(self):
        self._some_val = None
        
        super().__init__("YEAST", True)
        
        @characteristic("YST0", CharFlags.READ)
        def readonly_characteristic(self, options):
            return bytes("Hello World!", "utf-8")
        
        @readonly_characteristic.setter
        def writeonly_characteristic(self, value, options):
            self._some_value = value
            
        @descriptor("YST2", readonly_characteristic, DescFlags.READ)
        def readonly_descriptor(self, options):
            return bytes("This characteristic is completely pointless!", 'utf-8')
        
        
