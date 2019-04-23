#include <Time.h>
float current_v_right = 0;
float current_v_left = 0;
float old_v_right = 0;
float old_v_left = 0;
float c_right = 0;
float c_left = 0;
float to_left = millis(); // "old time"
float to_right = millis();  
float dist_pp = 0.55*3.1415926535/29;
float a_left = 0;
float a_right = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin (9600);
  pinMode(2, INPUT_PULLUP);           // set pin to input
  pinMode(3, INPUT_PULLUP);           // set pin to input
  attachInterrupt(digitalPinToInterrupt(2), updateright, RISING);
  attachInterrupt(digitalPinToInterrupt(3), updateleft, RISING);
 
}


void loop() {
  // put your main code here, to run repeatedly:

  String s = (String) current_v_left + " " + current_v_right; // Orig. Output for cam
  //String s = (String) "current_v_left:" + current_v_left + " current_v_right:" + current_v_right + " c_left:" + c_left + " c_right:" + c_right;
  Serial.println(s);

  if (current_v_left + a_left * (millis() - to_left) < 0) {
    current_v_left = 0;
    a_left = 0;
    
  }

  if (current_v_right + a_right * (millis() - to_right) < 0) {
    current_v_right = 0;
    a_right = 0;
  }

}

void updateleft(){
  c_left++;
  
  float tc_left = millis();
  current_v_left = dist_pp/(tc_left - to_left)*1000*3.6;
  
  a_left = (current_v_left - old_v_left) / (tc_left - to_left);

  old_v_left = current_v_left;
  to_left = tc_left;
}

void updateright(){
  c_right++;

  float tc_right = millis();
  current_v_right = dist_pp/(tc_right - to_right)*1000*3.6;
  
  a_right = (current_v_right - old_v_right) / (tc_right - to_right);

  old_v_right = current_v_right;  
  to_right = tc_right;
}
