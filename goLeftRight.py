import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# URI of the Crazyflie (radio link)
URI = 'radio://0/80/2M'

# Initialize the drivers for Crazyflie communication
cflib.crtp.init_drivers()

def left_right_movement():
    try:
        with SyncCrazyflie(URI, Crazyflie()) as scf:
            cf = scf.cf
            print("Calibrating sensors...")
            cf.param.set_value('kalman.resetEstimation', '1')
            time.sleep(0.1)
            cf.param.set_value('stabilizer.estimator', '2')  # Kalman estimator

            with MotionCommander(scf) as mc:
                print("Taking off...")

                # Take off and hover at 1 meter
                mc.take_off(height=1.0, velocity=0.5)
                time.sleep(9)  # Hover for stability

                print("Moving left...")
                mc.left(distance=0.5, velocity=0.5)  # Move left by 0.5 meters
                time.sleep(2)  # Allow time for movement

                print("Moving right...")
                mc.right(distance=0.5, velocity=0.5)  # Move right by 0.5 meters
                time.sleep(2)  # Allow time for movement

                print("Landing...")
                mc.land(velocity=0.3)  # Smooth landing
                time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            mc.land(velocity=0.3)
        except:
            print("Failed to land the Crazyflie!")

if __name__ == '__main__':
    print(f"Connecting to Crazyflie at {URI}...")
    left_right_movement()
    print("Flight complete.")
