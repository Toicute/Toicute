#include <Servo.h> 
#include <stdio.h>

Servo myservo1; 
Servo myservo2;

//Khai báo chân

int servo1 = 9;
int servo2 = 10;
int sensor = 5; 
int pos = 0;
int x;
//int z;

void setup() { 
    myservo1.attach(servo1);
    myservo2.attach(servo2);
    pinMode(sensor,INPUT);
    digitalWrite(sensor, 1);
    Serial.begin(9600);
} 

void loop() { 
//  Serial.println(digitalRead(sensor));
  // Đọc ký tự từ Serial rồi chuyển sang int
  x = Serial.readString().toInt();
  // Nếu sensor phát hiện vật thì gửi số 9 vào Serial ở dòng mới
  if (digitalRead(sensor)==LOW)
  {
    Serial.println('9');
    delay(5000);
  }
  // Nếu đọc được số 3 ở Serial thì cho motor1 quay
  if (x==3)
  {
    
    myservo1.write(90);
    delay(250);
    myservo1.write(0);
    delay(250);
//    Serial.print("8");
  }
  //Nếu đọc được số 4 ở Serial thì cho motor2 quay
  if (x==4)
  {
   
    myservo2.write(90);
    delay(250);
    myservo2.write(0);
    delay(250);
    Serial.println("7");
  }
}
