#define sensor 5
void setup()
{
  pinMode(sensor,INPUT);
  Serial.begin(9600);
  digitalWrite(sensor, 1);
}
void loop()
{
  Serial.print("Gia tri cam bien:");
  Serial.println(digitalRead(sensor)); //Nếu sensor = 1 thì không phát hiện vật cản, nếu sensor = 0 thì phát hiện vật cản.
  delay(100);
}
