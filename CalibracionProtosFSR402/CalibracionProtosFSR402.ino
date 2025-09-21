int muxSIG = A0; //Pin analogo para lectura de voltaje
const int muxS0 = 9; //Pin1 digital para selector del MUX
const int muxS1 = 10; //Pin2 digital para selector del MUX
String out = "";  //Variable de salida por transmisión serial

int lectura; //
float valor = 0; //

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
  //delay(10);
  //calibracion(1);
  //delay(10);
  //calibracion(2);
  //delay(10);
  //calibracion(3);
  //delay(10);
  funcionamiento();//Funcionamiento con rectas interpoladas de la calibración
}

void funcionamiento(){ //Funcion para funcionamiento normal del circuito
  for (int i = 0; i < 4; i++){ //Ciclo para leer los 4 sensores de presión
    out = out + "Sensor" + String(i+1) + ": " ; //Guarda que sensor actualmente se esta leyendo
    SetMuxChannel(i); //Canal de lectura
    lectura = analogRead(muxSIG); //Lectura del valor ingresado por el puerto analogo
    if(lectura>154){
      switch(i){
        case 0:
          valor = (lectura + 186.73)/0.6888;
          valor = valor*0.00981;
        break;
        case 1:
          valor = (lectura + 105.18)/0.6075;
          valor = valor*0.00981;
        break;
        case 2:
          //Sensor no calibrado correctamente
          valor = lectura;
        break;
        case 3:
          valor = (lectura + 14.404)/0.4754;
          valor = valor*0.00981;
        break;
        default:
          valor = 0;
      }   
    }else{
      valor = 0;
    }   
    out = out + String(valor) + " " ; //Se agrega a la salida el valor leido por el ADC del sensor actual
    delay(150); //Espera para conversion del ADC
  }
  //out = out +"\n";
  Serial.println(out); //Salida con el valor de los 4 sensores enviada por el serial
  out = "" ; //Se limpia la variable para una salida nueva
  delay(500); //Espera para siguente salida 
}

void calibracion(int canal){ //Funcion para funcionamiento continuo de un canal para calibrar sensores con el circuito
    SetMuxChannel(canal); //Canal seleccionado para el MUX
    lectura = analogRead(muxSIG); //Lectura del puerto analogo
    valor = lectura;  //Lectura guardada como valor actual
    out = "Sensor " + String(canal+1) + ": " + String(valor); //Guarda que sensor actualmente se esta leyendo
    delay(50); //Espera para conversion del ADC
    //Serial.println(lectura); //Salida con el valor medido por el conversor ADC
    Serial.println(out); //Salida con el valor de los 4 sensores enviada por el serial
    out = "" ;  //Se limpia la variable para una salida nueva
    delay(500); //Espera para siguente salida0
  }

void SetMuxChannel(int channel) //Creación de selector de MUX
{
  byte S0 = bitRead(channel,0);
  digitalWrite(muxS0, S0);
  byte S1 = bitRead(channel,1);
  digitalWrite(muxS1, S1);
  delay(200);
}
