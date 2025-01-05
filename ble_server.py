from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import NoIoAgent
from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)

# Define UUIDs - using standard 16-bit UUIDs for testing
TEST_SERVICE_UUID = "180D"  # Heart Rate Service UUID
TEST_CHAR_UUID = "2A37"     # Heart Rate Measurement Characteristic UUID

class TestService(Service):
    def __init__(self):
        # Initialize with the Heart Rate Service UUID
        super().__init__(TEST_SERVICE_UUID, True)
        
        # Add the characteristic to the service and store it
        self.test_characteristic = self.create_characteristic()

    @characteristic(TEST_CHAR_UUID, CharacteristicFlags.READ | CharacteristicFlags.WRITE | CharacteristicFlags.NOTIFY)
    def create_characteristic(self):
        # The value managed by this characteristic
        self._value = bytes([0x00])
        return self

    # Method will be called when a read is requested by the client
    def read(self):
        logging.info(f"Read request received, current value: {self._value.hex()}")
        return self._value

    # Method will be called when a write is requested by the client
    def write(self, value):
        logging.info(f"Write request received with value: {value.hex()}")
        self._value = value
        # Notify subscribers if the value changed
        self.notify_subscribers(value)

async def main():
    # Create our service
    service = TestService()
    
    # Create advertisement
    advertisement = Advertisement(local_name="PythonBLE", appearance=0)
    
    # Create our agent for handling pairing
    agent = NoIoAgent()
    
    # Start bluetooth service and register our things
    async with await service.start() as manager:
        # Power on adapter
        await manager.power_on()
        
        # Register our agent for handling pairing
        await agent.register(manager)
        
        adapter = manager.adapter
        logging.info(f"Adapter {adapter.address} / {adapter.name} ready")
        
        # Register advertisement
        await advertisement.register(adapter)
        logging.info("Advertisement registered")
        
        # Run forever
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopping...")