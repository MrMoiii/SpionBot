from sys import stdout
from sys import exit as sexit
import RPi.GPIO as GPIO
import pigpio
import robot as bot
from time import sleep
import requests
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<head>
<title>Let's go</title>
</head>
<body>
<style type="text/css">
.rotate180 {
    -webkit-transform: rotate(180deg);
    -moz-transform: rotate(180deg);
    -o-transform: rotate(180deg);
    -ms-transform: rotate(180deg);
    transform: rotate(180deg);
}</style>
<img src="stream.mjpg" width="640" height="480" class="rotate180"/>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def echo(s : str):
	stdout.write(s)

def main() -> int:

	echo("Hello world\n")
	GPIO.setmode(GPIO.BCM)

	####ROBOT ROUES
	GPIO.setup(14, GPIO.OUT)
	GPIO.setup(22, GPIO.OUT)
	GPIO.setup(17, GPIO.OUT)
	GPIO.setup(27, GPIO.OUT)

	###TEST/END
	GPIO.setup(18, GPIO.IN)
	GPIO.setup(23, GPIO.IN)

	###SERVO
	
	pwm = pigpio.pi()
	pwm.set_mode(18, pigpio.OUTPUT)
	pwm.set_PWM_frequency( 18, 50 )
	#pwm2 = pigpio.pi()
	#pwm2.set_mode(23, pigpio.OUTPUT)
	#pwm2.set_PWM_frequency( 23, 50 )

	motor_b_i = 500
	motor_h_i = 1500
	echo("start in 2s\n")
	sleep(2)
	pwm.set_servo_pulsewidth( 18, 1500 )
	#pwm2.set_servo_pulsewidth( 23, 1500 )

	GPIO.output( 22, 0)
	GPIO.output( 17, 0)
	GPIO.output( 14, 0)
	GPIO.output( 27, 0)
	sleep(0.5)

	#SERVER SETUP
	ip="192.168.192.233"
	port=80
	url ="http://{0}:{1}".format(ip,port)
	echo("ready\n")
	while True:
		try:

			inp = int(requests.get(url).text)
			#echo(f'{inp}\n')
			if(inp ==1):
				bot.avant(GPIO)
			if(inp ==3):
				bot.arriere(GPIO)
			if(inp ==4):
				bot.gauche(GPIO)
			if(inp ==5):
				bot.droite(GPIO)
			if(inp ==9):
				bot.stop(GPIO)

			if(inp == 8):
				if (motor_b_i <= 2500-150):
					motor_b_i += 150
					pwm.set_servo_pulsewidth( 18, motor_b_i )
					
			if(inp == 10):
				if (motor_b_i >= 500+150):
					motor_b_i -= 150
					pwm.set_servo_pulsewidth( 18, motor_b_i )
					
			"""
			if(inp == 6):
				if (motor_h_i <= 2500):
					motor_h_i += 100
					#pwm2.set_servo_pulsewidth( 23, motor_h_i )
					echo(f'{1}'.format(motor_h_i))
					
			if(inp == 2):
				if (motor_h_i > 510):
					motor_h_i -= 100
					#pwm2.set_servo_pulsewidth( 23, motor_h_i )
					echo(f'{1}\n'.format(motor_h_i))
			"""
				
		except KeyboardInterrupt:
			GPIO.cleanup()
			pwm.set_PWM_dutycycle( 18, 0 )
			pwm.set_PWM_dutycycle( 23, 0 )
			return 0
		except:
			pass
	GPIO.cleanup()
	return 0

if __name__ == '__main__':
	sexit(main())
