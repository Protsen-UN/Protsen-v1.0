const int sen1 = A0;//Declaración pin sensor 1
const int sen2 = A1;//Declaración pin sensor 2

const int s1Red = 3;//Declaración salida R sensor 1
const int s1Grn = 5;//Declaración salida G sensor 1

const int s2Red = 9;//Declaración salida R sensor 2
const int s2Grn = 10;//Declaración salida G sensor 2

void setup() {
  // put your setup code here, to run once:
  pinMode(sen1, INPUT);//Entrada Analoga Sensor 1
  pinMode(sen2, INPUT);//Entrada Analoga Sensor 2
  Serial.begin(9600); //Comienzo de transmisión serial a 9600 baudios
  delay (1000); //Espera para comenzar transmisión por el serial
}

void loop() {
  //Lectura primer sensor
  int sensor_1 =analogRead(sen1);
  //Impresión en el puerto serial del valor del sensor 1
  Serial.println("Sensor 1= "+String(sensor_1));
  
  //Lectura segundo sensor
  int sensor_2 =analogRead(sen2);
  //Impresión en el puerto serial del valor del sensor 2
  Serial.println("Sensor 2= "+String(sensor_2));

  //Calculo valores R y G para sensor 1
  int R1 = (sensor_1/10);
  int G1 = 100-(sensor_1/10);

  //Calculo valores R y G para sensor 2
  int R2 = (sensor_2/10);
  int G2 = 100-(sensor_2/10);
  
  //Cambio color LED RGB Sensor 1
  analogWrite(s1Red,255-R1);
  analogWrite(s1Grn,255-G1);

  //Cambio color LED RGB Sensor 2
  analogWrite(s2Red,255-R2);
  analogWrite(s2Grn,255-G2);

  //Espera siguiente toma de datos
  delay(25);
}
