#include <Arduino.h>

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    Serial.println("Message 1");
    delay(1000);
    Serial.println("Message 2");
    delay(1000);
    Serial.println("Message 3");
    delay(1000);
    Serial.println("Message 4");
    delay(1000);
}