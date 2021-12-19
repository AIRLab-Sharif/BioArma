long int time_now;
int data;
long long int out;

void setup () 
  {
  Serial.begin(9600);       
  Serial.println("Frequency Counter");
  } // end of setup
long int y(int x){
  long int out;
  out = (long int) (0.5*x)*(0.5*x)/50;
  
  return(out);
};

void loop () 
  {
  time_now = millis();
    
    if(time_now%2000<400){
      data = 600;
    }    
    else if(time_now%2000<1600){
     data = (abs(time_now%2000-1000));
    }
    else if(time_now%2000>1600){
    data = 600;
    };
//    out = data*data;
  Serial.println(y(data));


  // let serial stuff finish
  delay(200);
  }   // end of loop
