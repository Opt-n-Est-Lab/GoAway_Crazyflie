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
                
                # Increase takeoff height for more thrust
                mc.take_off(height=1.5, velocity=1.5)  # Try a higher height to generate more thrust
                time.sleep(10)  # Hover for 5 seconds

                print("Hovering...")
                time.sleep(3)  # Hover for stability

                print("Landing...")
                mc.land()
                time.sleep(2)  # Allow time for safe landing

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Attempting to land...")
        try:
            mc.land()
        except:
            print("Failed to land the Crazyflie!")

if __name__ == '__main__':
    print(f"Connecting to Crazyflie at {URI}...")
    simple_takeoff_landing()
    print("Flight complete.")
