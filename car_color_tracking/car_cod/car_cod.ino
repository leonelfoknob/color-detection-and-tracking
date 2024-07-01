int In1 =4 ;
int In2 =5 ;
int EnA =3 ;
int In3 =7 ;
int In4 =8 ;
int EnB =6 ;

int hiz = 150;

String komut;
int x;

void setup() {
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available()){
    x = Serial.read();
    if(x != 10){
      Serial.print(x);
       if(x == 119){ //ileri w
      //Serial.println("ilere komut");
      forward();
    }
    else if(x == 115){ //geri s
      //Serial.println("geri komut");
      back();
    }
    else if(x == 97){ //sol a
      //Serial.println("sol komut");
      left();
    }
    else if(x == 100){ //sağ d
      //Serial.println("sag komut");
      right();
    }
    else if(x == 113){ //durmak //q
      //Serial.println("stop komut");
      stoped();
    }
    else{
      //Serial.println("gecersiz komut");
    }
  }
    }
    //komut = Serial.readStringUntil('\n');
    //Serial.println(komut);
   /* if(komut == "w"){ //ileri
      //Serial.println("ilere komut");
      forward();
    }
    else if(komut == "s"){ //geri
      //Serial.println("geri komut");
      back();
    }
    else if(komut == "a"){ //sol
      //Serial.println("sol komut");
      left();
    }
    else if(komut == "d"){ //sağ
      //Serial.println("sag komut");
      right();
    }
    else if(komut == "q"){ //durmak
      //Serial.println("stop komut");
      stoped();
    }
    else{
      //Serial.println("gecersiz komut");
    }
  }*/
  
}


void stoped(){
  analogWrite(EnA,0);
  digitalWrite(In1,0);
  digitalWrite(In2,1);
  analogWrite(EnB,0);
  digitalWrite(In3,0);
  digitalWrite(In4,1);
}

void forward(){
  analogWrite(EnA,hiz);
  digitalWrite(In1,1);
  digitalWrite(In2,0);
  analogWrite(EnB,hiz);
  digitalWrite(In3,0);
  digitalWrite(In4,1);
}

void back(){
  analogWrite(EnA,hiz);
  digitalWrite(In1,0);
  digitalWrite(In2,1);
  analogWrite(EnB,hiz);
  digitalWrite(In3,1);
  digitalWrite(In4,0);
}

void right(){
  analogWrite(EnA,hiz);
  digitalWrite(In1,0);
  digitalWrite(In2,1);
  analogWrite(EnB,hiz);
  digitalWrite(In3,0);
  digitalWrite(In4,1);
}

void left(){
  analogWrite(EnA,hiz);
  digitalWrite(In1,1);
  digitalWrite(In2,0);
  analogWrite(EnB,hiz);
  digitalWrite(In3,1);
  digitalWrite(In4,0);
}
