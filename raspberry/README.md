# Raspberry
Mise en place de la partie raspberry du projet.

## Prérequis
Vous avez besoin:
* Le logiciel [MobaXterm](https://mobaxterm.mobatek.net/) pour faciliter la navigation via ssh dans la raspberry.
* Le matériel suivant:
  * 1 Raspberry Pi Zero
  * 1 [ESIEA Bot](https://esieabot.esiea.fr/fr/home-fr/)
  * 2 servomoteurs 9g
  * 1 camera adaptée

## Indication branchement
Suivre la notice d'assemblage [ici](https://esieabot.esiea.fr/fr/documentation-fr/)

* À la différence de l'ESIEA Bot, les pins utilisés pour le déplacement sont:
  * 14 Roue droite - avant
  * 27 Roue gauche - avant
  * 22 Roue droite - arrière
  * 17 Roue gauche - arrière

* Pour les servomoteurs :
  * 12 servo du bas
  * 13 servo du haut
  
## Installation
Installer via la commande ```git clone https://github.com/MrMoiii/SpionBot/raspberry```<br />

Pour utiliser le programme vous devez installer les librairies python suivantes:<br />
```sudo pip install pigpio requests picamera systemd-socketserver```<br />
 
## Usage

1. Connecter la arduino et la raspberry au même réseau<br />
2. Insérer l'IP de l'arduino dans ```ip``` en dessous de ```#SERVER SETUP```. <br />
3. lancer le programme avec la commande ```./run.sh``` (ne pas oublier chmod)<br />

Si l'ESIEA bot ne bouge pas au bout de 5 secondes, c'est qu'il n'a pas trouvé l'Arduino. Vérifier qu'elle soit bien connectée et redémarrer le programme.

