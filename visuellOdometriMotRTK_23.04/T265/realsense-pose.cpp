// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2019 Intel Corporation. All Rights Reserved.
#include <librealsense2/rs.hpp>
#include <iostream>
#include <iomanip>
#include <fstream>

#include <chrono>
#include <ctime>

#include <thread>
#include <mutex>
#include <cstring>
#include <cmath>

#include <unistd.h>

#include "cArduino.h"
#include "motion.h"

#include <cfloat>

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <termios.h>

#include <cstring>
#include <mutex>



#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <strings.h>

#include <iostream>

float PI = 3.141592653589793238462643383;


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


std::string fToString(float f){

    std::ostringstream strs;
	strs << std::setprecision(3) << std::fixed << f;
	return strs.str();

}

int main(int argc, char * argv[]) try {
    
        if(argc < 2){
        std::cout << "Skriv argument för programmet, "
                  << "1/0 för hjul odo, 1/0 för predict-pose"
                  << std::endl;
        }
        
       // cArduino arduino(ArduinoBaundRate::B9600bps);
        
        serial s("/dev/ttyACM0");
        rs2::pipeline pipe;
        rs2::config cfg;
        rotation_estimator algo;
        
        cfg.enable_stream(RS2_STREAM_POSE, RS2_FORMAT_6DOF);
        cfg.enable_stream(RS2_STREAM_ACCEL, RS2_FORMAT_MOTION_XYZ32F);
        cfg.enable_stream(RS2_STREAM_GYRO, RS2_FORMAT_MOTION_XYZ32F);  
      
        
        auto pf = pipe.start(cfg);
          
        rs2::device dev = pf.get_device();
        auto wheel_odom_snr = dev.first<rs2::wheel_odometer>();
       
       
        //std::ifstream calibrationFile("../forward_calib.json"); 
        std::ifstream calibrationFile("T265/forward_calib.json");
       // std::ifstream calibrationFile("T265/calibration_odometry.json");
        //std::ifstream calibrationFile("T265/rightward_calib.json");
      // std::ifstream calibrationFile("../downward_calib.json");
      //  std::ifstream calibrationFile("realsenset265/calibration_odometry.json");
        const std::string json_str((std::istreambuf_iterator<char>(calibrationFile)),
                          std::istreambuf_iterator<char>());
                  
        const std::vector<uint8_t> wo_calib(json_str.begin(), json_str.end());
     
        wheel_odom_snr.load_wheel_odometery_config(wo_calib);
        
        
        std::string temp;
        std::string::size_type sz,sz1,sz2;
        
        float speed1 = 0;
        float speed2 = 0;        
        
        rs2_vector sp1 = {0,0,0};
        rs2_vector sp2 = {0,0,0};
        
        
        rs2_vector sp1_o = {0,0,0};
        rs2_vector sp2_o = {0,0,0};
        
        int count1 = 0;
        int count2 = 0;
        
        while (true) {
            
            //testa att göra if satser på alla dessa för att kontrollera vilken frame det igentligen är!
            auto frames = pipe.wait_for_frames();

            auto f = frames.first_or_default(RS2_STREAM_POSE);
            auto g = frames.first_or_default(RS2_STREAM_GYRO);
            auto a = frames.first_or_default(RS2_STREAM_ACCEL);
          
            auto fp = f.as<rs2::pose_frame>();
            
            auto pose_data = fp.get_pose_data();
            
                
           
            auto gyro_f = g.as<rs2::motion_frame>();
            auto accel_f = a.as<rs2::motion_frame>();
                
           
            double ts = gyro_f.get_timestamp();
            rs2_vector gyro_data = gyro_f.get_motion_data();
            algo.process_gyro(gyro_data, ts);
            
              
            rs2_vector accel_data = accel_f.get_motion_data();
            algo.process_accel(accel_data);
           
	        do{
	            temp = s.sread();
	        } while(temp.size()< 9);
	       
		 
		     double theta = (PI/2)+algo.get_theta().y;
		     
		     //if(theta > )
		     
	        //arduino.flush();
	      	//std::this_thread::sleep_for(std::chrono::milliseconds(100));	
	        //std::cout << temp << std::endl;
	        //std::cout << temp.size() << std::endl;
	        if(temp.size() > 9){
            //std::cout << "Hastighet " << temp << std::endl;
		        try{
		        
		            //speed1 = 10.5;
		            //speed2 = 10.5;
		            speed1 = std::stof (temp,&sz);
		            speed2 = std::stof (temp.substr(sz),&sz1);
		            
		            count1 = std::stof (temp.substr(sz+sz1),&sz2);
		            count2 = std::stof (temp.substr(sz+sz1+sz2));
		            
		          //  std::cout << "Hastighet " << speed1 << " " << speed2 << std::endl;
		            
		            //FORWARD
		            sp1 = {cos(theta) * speed1, 0, sin(theta) * speed1 };
		            sp2 = {cos(theta) * speed2, 0, sin(theta) * speed2 };
		            
		            //sp1 = {10.0, 10.0 ,10.0 };
		            //sp2 = {10.0, 10.0 ,10.0 };
		            
		            
		            //RIGHT
		            //sp1 = {cos(algo.get_theta().y) * speed1, 0 ,sin(algo.get_theta().y) * speed1 };
		            // sp2 = {cos(algo.get_theta().y) * speed2, 0 ,sin(algo.get_theta().y) * speed2 };

                 
		            
		            //DOWN
		            //sp1 = {sin(algo.get_theta().y) * speed1, cos(algo.get_theta().y) * speed1 ,0 };
		            //sp2 = {sin(algo.get_theta().y) * speed2, cos(algo.get_theta().y) * speed1 ,0 };
		            
		            sp1_o = sp1;
		            sp2_o = sp2;
		            
		        } catch(const std::exception& e){
			        //std::cout <<"exception:("<< e.what() <<std::endl;
			        //ifall kraschar pga illegal rs2_vector värde eller core dump avkommentera undre
			        sp1 = sp1_o;
			        sp2 = sp1_o;
		            }
		    }
		    
            if(strcmp(argv[1],"1") == 0){
                bool b1 = wheel_odom_snr.send_wheel_odometry(0, f.get_frame_number(), sp1);
                bool b2 = wheel_odom_snr.send_wheel_odometry(1, f.get_frame_number(), sp2);
            }
            
            if(strcmp(argv[2],"1") == 0){
                auto now = std::chrono::system_clock::now().time_since_epoch();
                double now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(now).count();
                double pose_time_ms = fp.get_timestamp();
                float dt_s = static_cast<float>(std::max(0., (now_ms - pose_time_ms)/1000.));
                pose_data = predict_pose(pose_data, dt_s);
            }
		    
		    auto ms = std::chrono::duration_cast< std::chrono::milliseconds >(std::chrono::system_clock::now().time_since_epoch());


            //std::cout << std::setprecision(3) << std::fixed << theta << " cos,x: " << cos(theta) << " sin,z: " << sin(theta) << " T265 hast: " << pose_data.velocity << std::endl; 

            std::cout   << std::setprecision(3) << std::fixed << 
                    "tid: " << ms.count() <<
                    " Pose: "  << pose_data.translation.x << " " << pose_data.translation.y << " " << pose_data.translation.z << 
                    " Vinkel: " << theta << 
                    " confidence " << pose_data.tracker_confidence <<
                    "     Sp1: " << sp1 <<
                    "  T265 sp: " << pose_data.velocity << " " << count1 << " " << count2 << 
                    "     Sp2: " << sp2  << std::endl;
        
            }
        
        return EXIT_SUCCESS;
}
catch (const rs2::error & e) {
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e) {
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
  
