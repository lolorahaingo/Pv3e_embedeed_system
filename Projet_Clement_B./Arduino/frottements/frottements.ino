/*
   ######  #### ######## ########     ###                  ########  ##     ##  #######  ########
  ##    ##  ##  ##       ##     ##   ## ##                 ##     ## ##     ## ##     ## ##
  ##        ##  ##       ##     ##  ##   ##                ##     ## ##     ##        ## ##
   ######   ##  ######   ########  ##     ##    #######    ########  ##     ##  #######  ######
        ##  ##  ##       ##   ##   #########               ##         ##   ##         ## ##
  ##    ##  ##  ##       ##    ##  ##     ##               ##          ## ##   ##     ## ##
   ######  #### ######## ##     ## ##     ##               ##           ###     #######  ########

   SiERA - PV3e 2018 - ça frotte.

   Name:        Frottements
   Purpose:     .


   Author:      cmlgid

   Created:     24/02/2019
   Copyright:   (c) cmlgid 2019
   Licence:

   Revision 0.1 need test
*/
#define COEFVITESSE 0.33923 //(2 * Pi * fRayon) / iNombreDents * 3.6

#include <math.h>

const int pinInterrupt = 19;
int iNombreDents = 1;
float fRayon = 0.425 / 0.5;

volatile long lTick = 0;

float timerSpeed;
float rpmTachimeter;
float lastRPM;
float vitesseTachimetre;

void setup() {

    Serial.begin(115200);

    while (!Serial) {}

    pinMode(pinInterrupt, INPUT);

    attachInterrupt(digitalPinToInterrupt(pinInterrupt), updateTick, RISING);
}

void loop() {
    hallSpeed();
    if (isUpdated()) {
      Serial.print(millis());
      Serial.print("   ");
      Serial.print(rpmTachimeter);
      Serial.print("   ");
      Serial.print(vitesseTachimetre);
      Serial.println();
    }

}


void hallSpeed() {
  //Si deux dents comptées, on met à jour la vitesse de rotation
  lastRPM = rpmTachimeter;
  if (lTick >= 2) {
    timerSpeed = millis() - timerSpeed;
    rpmTachimeter = ((float)lTick / (float)iNombreDents) * 1000 / timerSpeed  * 60; //On divise le nombre de dents comptées en timerSpeed par le nombre de dents totales, on multiplie par 60 pour obtenir des rpm
    vitesseTachimetre = (rpmTachimeter / 60.0) * fRayon * M_PI * 3.6;
    // vitesseTachimetre = (((float)lTick / (float)iNombreDents) * 1000 / timerSpeed * fRayon * M_PI) * 3.6;
    // vitesseTachimetre = (((float)lTick / (float)iNombreDents) * 1000 / timerSpeed);
    lTick = 0;
    timerSpeed = millis();
  } else if (millis() - timerSpeed > 1000) {
    rpmTachimeter = 0;
    vitesseTachimetre = 0;
  }
}

boolean isUpdated() {
  return (lastRPM == rpmTachimeter) ? true : false;
}

void updateTick() {
    lTick++;
}
