int Distance = 0;
String command;
bool run_allowed = false;
bool full_rot_allowed = false;
int delaytime = 500;
int steps = 1200;
int times_angle_rot = 0;
int times_full_rot = 3600;
int counter_full_rot = 0;
int counter_angle_rot = 0;

void schritt_rl(){

    if (digitalRead(9) == LOW) {
      digitalWrite(9, HIGH);
    }
        
    digitalWrite(8, HIGH);
    delayMicroseconds(100);
    digitalWrite(8, LOW);
    delayMicroseconds(100);
  }

void schritt_ll(){
    if (digitalRead(9) == HIGH) {
      digitalWrite(9, LOW);
    }
    digitalWrite(8, HIGH);
    delayMicroseconds(100);
    digitalWrite(8, LOW);
    delayMicroseconds(100);
  
}

void serial(){
  if (Serial.available()){

    command = Serial.readStringUntil('\n');
    command.trim();
  }

    if (command.equals("start")){
    run_allowed = true;
    command = "";
  }

    if (command.equals("stop")){
    run_allowed = false;
    command = "";
  }

    if (command.startsWith("allow_full_rot")){
     full_rot_allowed = true;
     command = "";
  }

    if(command.startsWith("n_allow_full_rot")){
      full_rot_allowed = false;
      command = "";
    }

    if (command.startsWith("steps")){
    command.remove(0,5);
    steps = command.toInt();
    command = "";
  }

      if (command.startsWith("delay")){
    command.remove(0,5);
    delaytime = command.toInt();
    command = "";
  }

      if (command.startsWith("times_full_rot")){
    command.remove(0,14);
    times_full_rot = command.toInt();
    command = "";
  }
}

void setup(){
  Serial.begin(9600);

  Serial.println("Test");

  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(8, OUTPUT);

  pinMode(9, OUTPUT);

  digitalWrite(8, LOW);

  digitalWrite(9, LOW);

  delay(2000);

}

void loop() {

  serial();
  if (run_allowed){
    if (full_rot_allowed){
      for(int i=0; i<steps;i++){
        schritt_rl();
        //Serial.println("RL");
      }
      
      delay(delaytime);
      
      for(int i=0; i<steps;i++){
        schritt_ll();
        //Serial.println("LL");
      }
      
      delay(delaytime);
      
      for(int i=0; i<times_full_rot*1600;i++){
        schritt_rl();
        //Serial.println("RLFull");
      }

      delay(delaytime);

      for(int i=0; i<times_full_rot*1600;i++){
        schritt_ll();
        //Serial.println("LLFull");
      }

      delay(delaytime);
      
    }else{
       for(int i=1; i<=steps; i++){
        schritt_rl();
        //Serial.println("RL");
      }
      
      delay(delaytime);
      
      for(int i=1; i<=steps; i++){
        schritt_ll();
        //Serial.println("LL");
      }
      delay(delaytime);
    }
  }
}
