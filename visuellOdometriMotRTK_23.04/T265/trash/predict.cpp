// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2019 Intel Corporation. All Rights Reserved.
#include <librealsense2/rs.hpp>
#include <iostream>
#include <iomanip>
#include <chrono>
#include <thread>
#include <mutex>
#include <string>
#include <fstream>
#include <cstring>
#include "cArduino.h"

#include <math.h>
#include <float.h>

static void toEulerAngle(const rs2_quaternion& q, double& roll, double& pitch, double& yaw)
{
	// roll (x-axis rotation)
	double sinr_cosp = +2.0 * (q.w * q.x + q.y * q.z);
	double cosr_cosp = +1.0 - 2.0 * (q.x * q.x + q.y * q.y);
	roll = atan2(sinr_cosp, cosr_cosp);

	// pitch (y-axis rotation)
	double sinp = +2.0 * (q.w * q.y - q.z * q.x);
	if (fabs(sinp) >= 1)
		pitch = copysign(M_PI / 2, sinp); // use 90 degrees if out of range
	else
		pitch = asin(sinp);

	// yaw (z-axis rotation)
	double siny_cosp = +2.0 * (q.w * q.z + q.x * q.y);
	double cosy_cosp = +1.0 - 2.0 * (q.y * q.y + q.z * q.z);  
	yaw = atan2(siny_cosp, cosy_cosp);
}


inline rs2_quaternion quaternion_exp(rs2_vector v)
{
    float x = v.x/2, y = v.y/2, z = v.z/2, th2, th = sqrtf(th2 = x*x + y*y + z*z);
    float c = cosf(th), s = th2 < sqrtf(120*FLT_EPSILON) ? 1-th2/6 : sinf(th)/th;
    rs2_quaternion Q = { s*x, s*y, s*z, c };
    return Q;
}

inline rs2_quaternion quaternion_multiply(rs2_quaternion a, rs2_quaternion b)
{
    rs2_quaternion Q = {
        a.x * b.w + a.w * b.x - a.z * b.y + a.y * b.z,
        a.y * b.w + a.z * b.x + a.w * b.y - a.x * b.z,
        a.z * b.w - a.y * b.x + a.x * b.y + a.w * b.z,
        a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
    };
    return Q;
}

rs2_pose predict_pose(rs2_pose & pose, float dt_s)
{
    rs2_pose P = pose;
    P.translation.x = dt_s * (dt_s/2 * pose.acceleration.x + pose.velocity.x) + pose.translation.x;
    P.translation.y = dt_s * (dt_s/2 * pose.acceleration.y + pose.velocity.y) + pose.translation.y;
    P.translation.z = dt_s * (dt_s/2 * pose.acceleration.z + pose.velocity.z) + pose.translation.z;
    rs2_vector W = {
            dt_s * (dt_s/2 * pose.angular_acceleration.x + pose.angular_velocity.x),
            dt_s * (dt_s/2 * pose.angular_acceleration.y + pose.angular_velocity.y),
            dt_s * (dt_s/2 * pose.angular_acceleration.z + pose.angular_velocity.z),
    };
    P.rotation = quaternion_multiply(quaternion_exp(W), pose.rotation);
    return P;
}

int main(int argc, char * argv[]) try
{
    
    cArduino arduino(ArduinoBaundRate::B9600bps);
    
    std::string temp;
    std::string::size_type sz;

    float sp1_x = 0;
    float sp1_z = 0;
    
    float sp2_x = 0;
    float sp2_z = 0;
    
    float speed1 = 0;
    float speed2 = 0;
    
    int fn = 0;
    
    rs2_vector sp1 = {sp1_x,0,sp1_z};
    rs2_vector sp2 = {sp2_x,0,sp2_z};
    
    rs2_pose predicted_pose;
    
    double roll,pitch,yaw;
    
    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Create a configuration for configuring the pipeline with a non default profile
    rs2::config cfg;
    // Add pose stream
    cfg.enable_stream(RS2_STREAM_POSE, RS2_FORMAT_6DOF);

    // Define frame callback
    // The callback is executed on a sensor thread and can be called simultaneously from multiple sensors
    // Therefore any modification to common memory should be done under lock
    std::mutex mutex;
    auto callback = [&](const rs2::frame& frame)
    {
        std::lock_guard<std::mutex> lock(mutex);
        if (rs2::pose_frame fp = frame.as<rs2::pose_frame>()) {
            rs2_pose pose_data = fp.get_pose_data();
            fn = fp.get_frame_number();
            auto now = std::chrono::system_clock::now().time_since_epoch();
            double now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();
            double pose_time_ms = fp.get_timestamp();
            float dt_s = static_cast<float>(std::max(0., (now_ms - pose_time_ms)/1000.));
            predicted_pose = predict_pose(pose_data, dt_s);
            toEulerAngle(predicted_pose.rotation, roll,pitch,yaw);
            std::cout << "Predicted " << std::fixed << std::setprecision(3) << dt_s*1000 << "ms " <<
                    "Confidence: " << pose_data.tracker_confidence << " T: " <<
                    predicted_pose.translation.x << " " <<
                    predicted_pose.translation.y << " " <<
                    predicted_pose.translation.z << " " <<
                    pose_data.translation.x << " " <<
                    pose_data.translation.y << " " <<
                    pose_data.translation.z << " " << " " << roll << " " << yaw << " " << pitch<<  std::endl;
        }
    };

    // Start streaming through the callback with default recommended configuration
    rs2::pipeline_profile pf = pipe.start(cfg, callback);
    std::cout << "started thread\n";
    
    rs2::device dev = pf.get_device();
    
    auto wheel_odom_snr = dev.first<rs2::wheel_odometer>();
    
    std::ifstream calibrationFile("../calibration_odometry.json");
    //std::ifstream calibrationFile("realsenset265/calibration_odometry.json");
    const std::string json_str((std::istreambuf_iterator<char>(calibrationFile)),
                      std::istreambuf_iterator<char>());
              
    const std::vector<uint8_t> wo_calib(json_str.begin(), json_str.end());
 
    wheel_odom_snr.load_wheel_odometery_config(wo_calib);
    
    
    std::this_thread::sleep_for(std::chrono::milliseconds(250));
    while(true) {
        temp = arduino.read();
	  	std::this_thread::sleep_for(std::chrono::milliseconds(10));	
	    if(temp.size() > 9){
		
		    try{	
		        //std::cout << temp << std::endl;
		        speed1 = std::stof (temp,&sz);
		        speed2 = std::stof (temp.substr(sz));
		        
		        toEulerAngle(predicted_pose.rotation, roll,pitch,yaw);
		        
		        sp1.x = sin(pitch) * speed1;
		        sp1.z = cos(pitch) * speed1;
		        
		        sp2.x = sin(pitch) * speed2; 
		        sp2.z = cos(pitch) * speed2;
		        
		        sp1_x = sp1.x;
		        sp1_z = sp1.z;
	        
		        sp2_x = sp2.x;
		        sp2_z = sp2.z;
		    } catch(const std::exception& e){
			    std::cout <<"exception:("<< e.what() <<std::endl;
			    sp1 = {sp1_x,0,sp1_z};
			    sp2 = {sp2_x,0,sp2_z};
		    }
		}
		
        if(strcmp(argv[1],"1") == 0){
            bool b1 = wheel_odom_snr.send_wheel_odometry(0, fn, sp1);
            bool b2 = wheel_odom_snr.send_wheel_odometry(1, fn, sp2);
        }
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error & e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
