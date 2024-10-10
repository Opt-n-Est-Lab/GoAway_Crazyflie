import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# URI of the Crazyflie (radio link)
URI = 'radio://0/80/2M'

# Initialize the drivers for Crazyflie communication
cflib.crtp.init_drivers()

def simple_takeoff_landing():
    try:
        with SyncCrazyflie(URI, Crazyflie()) as scf:
            cf = scf.cf
            print("Calibrating sensors...")
            cf.param.set_value('kalman.resetEstimation', '1')
            time.sleep(0.1)
            cf.param.set_value('stabilizer.estimator', '2')  # Kalman estimator
            
            print("Taking off with smooth thrust!")

            with MotionCommander(scf) as mc:
                # Smooth takeoff and hover
                mc.take_off()  # Smooth and slow takeoff
                time.sleep(5)  # Allow it to hover and stabilize

                print("Hovering...")
                time.sleep(5)  # More time to stabilize

                print("Landing...")
                mc.land()  # Slow and controlled landing
                time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            mc.land()
        except:
            print("Failed to land the Crazyflie!")

if __name__ == '__main__':
    print(f"Connecting to Crazyflie at {URI}...")
    simple_takeoff_landing()
    print("Flight complete.")
