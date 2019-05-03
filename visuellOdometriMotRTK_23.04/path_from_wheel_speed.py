import numpy as np

def path_from_wheel_speed(left_speed, right_speed, time):
    left_v = np.linalg.norm(left_speed, axis=1)
    right_v = np.linalg.norm(right_speed, axis=1)
    dt = np.diff(time)

    


