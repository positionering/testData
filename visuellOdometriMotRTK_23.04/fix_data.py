import numpy as np


def rotate_GPSdata(GPSdataV, GPSdataH):
    heading = GPSdataV[0,:] -  GPSdataH[0,:]
    
    heading = unit_vector(heading)

    heading = np.array([[0, 1], [-1, 0]]) @ heading

    theta = angle_between(heading, np.array([0,1]))

    theta = angle_between(np.array([1,0]), np.array([0,1]))

    rot = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])

    GPSdataV = center_data(GPSdataV)
    GPSdataH = center_data(GPSdataH)

    GPSdata = (GPSdataV + GPSdataH)/2

    return np.apply_along_axis(lambda arr: rot@arr, axis=1, arr=GPSdata)


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def center_data(data):
    if len(data.shape) == 1:
        data = data.reshape(len(data),1)
    for i in range(data.shape[1]):
            data[:,i] -= data[0,i]
    return data

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def main():
    t = np.array([5,6,7,9,12,34,45]).T
    path1 = np.array([[0,4,3,53,2,23,35],
                      [1,1,1,1,1,1,1]]).T
    path2 = np.array([[0,4,3,53,2,23,35],
                      [-1,-1,-1,-1,-1,-1,-1]]).T

    print(rotate_GPSdata(path1, path2))
    print(center_data(t))


if __name__ == "__main__":
       main()