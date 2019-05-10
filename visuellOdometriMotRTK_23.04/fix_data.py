import numpy as np


def fix_GPSdata(GPSdataV, GPSdataH, medel = 1):

    heading = np.array([[0,0]])
    for i in range(medel):
         heading = heading + (np.array([[0, 1], [-1, 0]]) @ unit_vector(GPSdataV[i,:] -  GPSdataH[i,:]))
    heading = heading / medel

    theta = angle_between(heading, np.array([0,1]))
    theta = np.copysign(theta, np.cross(heading, np.array([0,1])))

    GPSdataV = center_data(GPSdataV)
    GPSdataH = center_data(GPSdataH)

    GPSdata = (GPSdataV + GPSdataH)/2
    return rotate_2Ddata(GPSdata, theta)


def rotate_2Ddata(data, angle):
    rot = np.array([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]])
    return np.apply_along_axis(lambda arr: rot@arr, axis=1, arr=data)


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

    print(fix_GPSdata(path1, path2, 3))
    print(center_data(t))


if __name__ == "__main__":
       main()