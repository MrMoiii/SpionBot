# Arduino
Mise en place de la partie Arduino nano iot du projet.

## Installation
Vous avez besoin:
* Le logiciel [Arduino IDE](https://www.arduino.cc/en/software)
* Le matériel suivant:
  * Arduino nano iot
  * bouton poussoir
 
## Usage
Prérequis: Sur l’application Arduino IDE, aller dans outil, sélectionner gestionnaire de carte, taper arduino nano 33 IOT et trouver le paquet  « Arduino SAMD boards », puis revenir dans outil, aller dans gérer les bibliothèques, et ajouter : Wifinina, Adafruit_MPU6050 ; Adafruit_MPU6050, Adafruit_Unified_Sensor, MPU6050, Arduino_LSM6DS3, , Seeed_Arduino_LSM6DS3 qui sont nécessaire pour utiliser l’accéléromètre et la connection wifi. Puis dans outil aller dans type de carte puis Arduino SAMD et ensuite cliquer sur l’arduino nano 33 IoT, ensuite dans outil aller dans port et sélectionner la bonne COM .<br />

1. Dans le code, modifier ```TON SSID``` par le nom du reseau qui sera utilisé.<br />
2. Dans le code, modifier ```TON MDP``` par le mot de passe du reseau qui sera utilisé.<br />
3. Mettre en place un bouton poussoirs sur le pin ```2u``` de l'ardino nano iot (indiqué par ```SWITCH PIN``` dans le code)<br />
4. Televerser le programme.<br />
