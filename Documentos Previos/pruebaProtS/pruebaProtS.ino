int muxSIG = A0; //Pin analogo para lectura de voltaje
const int muxS0 = 9; //Pin1 digital para selector del MUX
const int muxS1 = 10; //Pin2 digital para selector del MUX
String out = "";  //Variable de salida por transmisión serial


int lectura; //
float valor = 0; //

int SetMuxChannel(byte channel) //Creación de selector de MUX
{
  digitalWrite(muxS0, bitRead(channel, 0)); 
  digitalWrite(muxS1, bitRead(channel, 1));
}

void setup()
{
  pinMode(muxSIG, INPUT); //Señal recibida por el multiplexor
  pinMode(muxS0, OUTPUT); //Señal de control 0 para el multiplexor
  pinMode(muxS1, OUTPUT); //Señal de control 1 para el multiplexor
  Serial.begin(9600); //Comienzo de transmisión serial a 9600 baudios
  delay (5000); //Espera para comenzar transmisión por el serial
 
}

void loop()
{
  //calibracion(0);
  funcionamiento();
}

void funcionamiento(){ //Funcion para funcionamiento normal del circuito
  for (byte i = 0; i < 4; i++){ //Ciclo para leer los 4 sensores de presión
    out = out + "Sensor" + String(i+1) + ": " ; //Guarda que sensor actualmente se esta leyendo
    SetMuxChannel(i); //Canal de lectura
    lectura = analogRead(muxSIG); //Lectura del valor ingresado por el puerto analogo
    valor = (lectura-264)*(1.0/1023.0)*11.0;
    valor = min(max(valor,0.0),11.0);
    out = out + String(valor) + " " ; //Se agrega a la salida el valor leido por el ADC del sensor actual
    delay(100); //Espera para conversion del ADC
  }
  Serial.println(out); //Salida con el valor de los 4 sensores enviada por el serial
  out = "" ; //Se limpia la variable para una salida nueva
  delay(600); //Espera para siguente salida 
}

void calibracion(int canal){ //Funcion para funcionamiento continuo de un canal para calibrar sensores con el circuito
    SetMuxChannel(canal); //Canal seleccionado para el MUX
    lectura = analogRead(muxSIG); //Lectura del puerto analogo
    valor = lectura;  //Lectura guardada como valor actual
    out = "Sensor " + String(canal+1) + ": " + String(valor); //Guarda que sensor actualmente se esta leyendo
    delay(100); //Espera para conversion del ADC
    //Serial.println(lectura); //Salida con el valor medido por el conversor ADC
    Serial.println(out); //Salida con el valor de los 4 sensores enviada por el serial
    out = "" ;  //Se limpia la variable para una salida nueva
    delay(900); //Espera para siguente salid
  }
