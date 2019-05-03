import numpy as np

def path_from_wheel_speed(speed, right, time):
    return np.cumsum((left_speed[:-1].T * np.diff(time)).T, axis=0)

    
if __name__ == "__main__":
    s = np.random.rand(10,2)
    t = np.random.rand(1,10)

    print(path_from_wheel_speed(s,t))

