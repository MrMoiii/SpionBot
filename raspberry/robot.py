
def droite(GPIO):
	GPIO.output( 22, 1)
	#GPIO.output( 17, 0)
	#GPIO.output( 14, 0)
	GPIO.output( 27, 1)

def gauche(GPIO):
	#GPIO.output( 22, 0)
	GPIO.output( 17, 1)
	GPIO.output( 14, 1)
	#GPIO.output( 27, 0)

def avant(GPIO):
	#GPIO.output( 22, 0)
	#GPIO.output( 17, 0)
	GPIO.output( 14, 1)
	GPIO.output( 27, 1)

def arriere(GPIO):
	GPIO.output( 22, 1)
	GPIO.output( 17, 1)
	#GPIO.output( 14, 0)
	#GPIO.output( 27, 0)

def stop(GPIO):
	GPIO.output( 22, 0)
	GPIO.output( 17, 0)
	GPIO.output( 14, 0)
	GPIO.output( 27, 0)