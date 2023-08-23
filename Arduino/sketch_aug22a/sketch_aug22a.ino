#include <ros.h>
//#include <std_msgs/String.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh;

//std_msgs::String str_msg;
//ros::Publisher chatter("chatter", &str_msg);

std_msgs::Float32 float_msg;
ros::Publisher distance("distance", &float_msg);

//char hello[13] = "Hello World!";

const int Trigger = 2; // Pin digital 2 para el trigger del sensor
const int Echo = 3; // Pin digital 3 para el Echo del sensor

void setup() {
  
  nh.initNode();
  //nh.advertise(chatter);
  nh.advertise(distance);

  pinMode(Trigger, OUTPUT); // Pin de salida
  pinMode(Echo, INPUT); // Pin de entrada
  digitalWrite(Trigger, LOW); // Inicializamos el pin con 0

}

void loop() {

  long t; // Tiempo que demora en llamar el eco
  long d; // Distancia en centímetros
  digitalWrite(Trigger, HIGH); 
  delayMicroseconds(10); // Enviams un pulso de 10us
  digitalWrite(Trigger, LOW);

  t = pulseln(Echo, HIGH); // Obtenemos el ancho del pulso
  d = t/59 // Escalamos el tiempo a una distancia en cm

  //str_msg.data = hello;
  //chatter.publish(&str_msg);
  float_msg.data = d
  chatter.publish(&float_msg);
  nh.spinOnce();
  delay(1000);
}