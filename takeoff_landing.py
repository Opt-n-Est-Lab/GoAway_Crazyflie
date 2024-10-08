import time
import cflib.crtp  # Crazyradio communication library
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# URI of the Crazyflie (radio link)
URI = 'radio://0/80/2M'  # Adjust this to your Crazyflie's URI

# Initialize the drivers for Crazyflie communication
cflib.crtp.init_drivers()

def simple_takeoff_landing():
    try:
        with SyncCrazyflie(URI, Crazyflie()) as scf:
            with MotionCommander(scf) as mc:
                print("Taking off with more thrust!")
                
                # Try increasing height and velocity to ensure enough thrust
                mc.take_off(height=1.0)  # Increased velocity
                time.sleep(5)  # Allow enough time to reach takeoff height

                print("Hovering...")
                time.sleep(5)  # Hover for stability

                print("Landing...")
                mc.land(velocity=0.3)  # Slow, controlled landing
                time.sleep(2)  # Allow time for safe landing

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Attempting to land...")
        try:
            mc.land(velocity=0.3)  # Ensure safe landing in case of error
        except:
            print("Failed to land the Crazyflie!")

if __name__ == '__main__':
    print(f"Connecting to Crazyflie at {URI}...")
    simple_takeoff_landing()
    print("Flight complete.")
