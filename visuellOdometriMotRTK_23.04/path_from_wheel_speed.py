import numpy as np

def path_from_wheel_speed(speed, time, start = np.array([0,0])):
    return (np.cumsum((speed[:-1,:].T * np.diff(time/1000)).T, axis=0) + start)

    
if __name__ == "__main__":
    s = np.random.rand(10,2)
    t = np.random.rand(1,10)

    print(path_from_wheel_speed(s,t))

