#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

Servo servo_x;
Servo servo_y;
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);

byte incomingByte;
float Lat,Long;

int motor_angle_x = 90;
int motor_angle_y = 90;

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.begin (16, 2);
  
  servo_x.attach(5);
  servo_y.attach(6);
  servo_x.write(motor_angle_x);
  servo_y.write(motor_angle_y);
}

void loop() {
  
  if (Serial.available() > 0 ) {
    incomingByte = Serial.read();
    if(incomingByte != 10){
    //Serial.println(incomingByte);
    lcd.setCursor(0, 0);
    lcd.print("cx:");
    lcd.print(incomingByte);
    lcd.print("  ");
    if(incomingByte == 115){//stop s
      motor_angle_x = 90;
      motor_angle_y = 90;
    }
    if(incomingByte == 99){//center c
      motor_angle_x = motor_angle_x;
      motor_angle_y = motor_angle_y;
    }
    else if(incomingByte == 114){ //right r
      motor_angle_x = motor_angle_x-1;
      if(motor_angle_x<=0){
        motor_angle_x = 0;
      }
    }
    else if(incomingByte == 108){//left l
      motor_angle_x = motor_angle_x+1;
      if(motor_angle_x>=180){
        motor_angle_x = 180;
      }
    }
    else if(incomingByte == 98){//bottom b
      motor_angle_y = motor_angle_y-1;
      if(motor_angle_y<=0){
        motor_angle_y = 0;
      }
    }
    else if(incomingByte == 116){//top t
      motor_angle_y = motor_angle_y+1;
      if(motor_angle_y>=180){
        motor_angle_y = 180;
      }
    }
    lcd.setCursor(0, 1);
    lcd.print("angle:");
    lcd.print(motor_angle_x);
    lcd.print("  ");
    
    servo_x.write(motor_angle_x);
    servo_y.write(motor_angle_y);
    //delay(20);
    }
  }
}
