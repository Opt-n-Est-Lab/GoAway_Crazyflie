import time
import cflib.crtp  # Crazyflie communication API
from cflib.crazyflie import Crazyflie
from cflib.positioning import PositionHlCommander  # For controlling position

# Initialize the low-level drivers
cflib.crtp.init_drivers()

class CrazyflieControl:
    def __init__(self, uri):
        self.uri = uri
        self.drone = Crazyflie(rw_cache='./cache')

        # Connect callbacks
        self.drone.connected.add_callback(self._connected)
        self.drone.disconnected.add_callback(self._disconnected)
        self.drone.connection_failed.add_callback(self._connection_failed)
        self.drone.connection_lost.add_callback(self._connection_lost)

    def connect(self):
        """Connect to the Crazyflie drone via USB."""
        print('Connecting to %s...' % self.uri)
        self.drone.open_link(self.uri)

    def _connected(self, link_uri):
        """Callback when the drone is connected."""
        print('Connected to %s' % link_uri)
        self.fly()

    def _disconnected(self, link_uri):
        """Callback when the drone is disconnected."""
        print('Disconnected from %s' % link_uri)

    def _connection_failed(self, link_uri, msg):
        """Callback when the connection fails."""
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        """Callback when the connection is lost."""
        print('Connection to %s lost: %s' % (link_uri, msg))

    def fly(self):
        """Control the drone's flight behavior."""
        with PositionHlCommander(self.drone) as commander:
            print("Taking off...")
            commander.take_off()

            try:
                # Add your flying logic here
                print("Hovering for 3 seconds...")
                time.sleep(3)

                print("Landing...")
                commander.land()
            except KeyboardInterrupt:
                print("Emergency landing!")
                commander.land()

# Main program execution
if __name__ == '__main__':
    # USB URI for connecting to the Crazyflie
    uri = 'usb://0'

    # Create the drone control object
    drone_control = CrazyflieControl(uri)

    # Connect to the Crazyflie drone
    drone_control.connect()

    # Keep the program running
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break
