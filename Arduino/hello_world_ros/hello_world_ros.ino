#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle nh; // Hacer nodo de ROS

std_msgs::Float32 float_msg;  // Hacer variable de tipo float
ros::Publisher distance("distance", &float_msg);  // Publisher para mandar la distancia

const int Trigger = 2; // Pin digital 2 para el trigger del sensor
const int Echo = 3; // Pin digital 3 para el Echo del sensor

void setup() {
  
  nh.initNode();  // Inicializar el codigo
  nh.advertise(distance);   // Iniciar el publisher

  pinMode(Trigger, OUTPUT); // Pin de salida
  pinMode(Echo, INPUT); // Pin de entrada
  digitalWrite(Trigger, LOW); // Inicializamos el pin con 0

}

void loop() {

  long t; // Tiempo que demora en llamar el eco
  long d; // Distancia en centímetros
  digitalWrite(Trigger, HIGH); // Mandar una señal
  delayMicroseconds(10); // Enviams un pulso de 10us
  digitalWrite(Trigger, LOW); // Apagar la señal

  t = pulseIn(Echo, HIGH); // Obtenemos el ancho del pulso
  d = t/59; // Escalamos el tiempo a una distancia en cm

  float_msg.data = d; // El mensaje a mandar es la distancia
  distance.publish(&float_msg); // Publicar el mensaje
  nh.spinOnce();
  delay(1000);

}
