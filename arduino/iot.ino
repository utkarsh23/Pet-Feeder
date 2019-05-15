#include <Servo.h>
#include <ESP8266WiFi.h>

Servo servo;
WiFiServer server(80);

// WiFi hotspot credentials
const char* ssid = "";
const char* password = "";

// PIN numbers
int pirPin = 14;
int servoPin = 16;
int redPin = 15;
int greenPin = 13;
int bluePin = 12;
int angle = 0;

void setup() {
    servo.attach(servoPin);
    servo.write(angle); 

    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    pinMode(pirPin,INPUT);

    Serial.begin(115200);

    // Connect to WiFi network
    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");

    // Start the server
    server.begin();
    Serial.println("Server started");

    // Print the IP address
    Serial.print("Use this URL : ");
    Serial.print("http://");
    Serial.print(WiFi.localIP());
    Serial.println("/");
}

void setColor(int redValue, int greenValue, int blueValue){
    analogWrite(redPin, redValue);
    analogWrite(greenPin, greenValue);
    analogWrite(bluePin, blueValue);
}

void servoRotate(){
    setColor(0, 255, 0);
    for(angle = 0; angle < 180; angle++){
        servo.write(angle);
        delay(15);
    }
    delay(2000);
    for(angle = 180; angle > 0; angle--){
        servo.write(angle);
        delay(15);
    }
    setColor(255, 0, 0);  
}

void loop() {
    setColor(255, 0, 0);
    delay(1000);

    if (digitalRead(pirPin)== LOW){
        Serial.println("Motion detected!");
        setColor(0, 0, 255);
        delay(3000);
    }

    WiFiClient client = server.available();
    if (!client) {
        return;
    }

    // Wait until the client sends some data
    Serial.println("new client");
    while (!client.available()) {
        delay(1);
    }

    // Read the first line of the request
    String request = client.readStringUntil('\r');
    client.flush();

    // Match the request
    if (request.indexOf("/?FEED") != -1) {
        servoRotate();
    }

    if (request.indexOf("/?DETECT") != -1) {
        setColor(153, 50, 204);
        delay(2000);
    }

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println(""); //  do not forget this one
    client.println("<!DOCTYPE HTML>");
    client.println("<html>Success");
    client.println("</html>");

    delay(1);
}
