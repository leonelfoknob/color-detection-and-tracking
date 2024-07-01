#include <Servo.h>

Servo servo_x;
Servo servo_y;
int pos_servo_x;
int pos_servo_y;

char Serparator = ',';
String receive_data;

int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  servo_x.attach(5);
  
  pos_servo_x = 90;
  pos_servo_y = 90;
  
  delay(3000);

} 

void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 /*receive_data = Serial.readStringUntil('\n');
 if (receive_data.length() > 0){
  pos_servo_x = (getValue(receive_data,Serparator, 0)).toInt(); //-1 gauche 1 droite
  pos_servo_y = (getValue(receive_data,Serparator, 1)).toInt(); //1 accelere -1 geri
  
 }*/
 servo_x.write(x);
 /*Serial.println(x);*/
}

 

//function to separate string separate by one charatere for each position's data
String getValue(String data, char separator, int index){
int found = 0;
int strIndex[] = {0, -1};
int maxIndex = data.length()-1;
for(int i=0; i<=maxIndex && found<=index; i++){
  if(data.charAt(i)==separator || i==maxIndex){
    found++;
    strIndex[0] = strIndex[1]+1;
    strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
}
return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
