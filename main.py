import time
import cflib.crtp  # Crazyflie communication API
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.positioning import PositionHlCommander  # Position control

# Initialize the low-level drivers
cflib.crtp.init_drivers()

# Threshold distance for the hand detection (in meters)
HAND_DISTANCE_THRESHOLD = 0.2  # 20 cm

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
        """Connect to the Crazyflie drone."""
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

    def get_proximity_data(self):
        """Simulate getting data from the proximity sensor.
        This should be replaced with real sensor data."""
        # Simulate the hand being close, change this value to test
        simulated_distance = 0.15  # Hand 15 cm away (less than threshold)
        return simulated_distance

    def fly(self):
        """Control the drone's flight behavior."""
        with PositionHlCommander(self.drone) as commander:
            print("Taking off...")
            commander.take_off()

            try:
                while True:
                    # Get proximity sensor data
                    proximity_distance = self.get_proximity_data()

                    if proximity_distance < HAND_DISTANCE_THRESHOLD:
                        print("Hand detected close! Moving back...")
                        # Move the drone backward (negative forward movement)
                        commander.forward(-0.2)  # Move back 20 cm

                    time.sleep(0.1)  # Adjust delay as necessary for responsiveness
            except KeyboardInterrupt:
                print("Landing...")
                commander.land()

# Main program execution
if __name__ == '__main__':
    # Replace with your Crazyflie drone's URI
    uri = 'radio://0/80/2M/E7E7E7E7E7'  # Example URI, adjust as per your setup

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
