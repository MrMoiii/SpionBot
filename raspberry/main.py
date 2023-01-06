from sys import stdout
from sys import exit as sexit
import RPi.GPIO as GPIO
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
	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(12, GPIO.OUT)
	motor_haut = GPIO.PWM(12, 50)
	motor_bas = GPIO.PWM(16, 50)
	motor_haut.start(0)
	motor_h_i = 0
	sleep(2)
	echo("sleep 2s\n")
	motor_bas.start(0)
	motor_b_i = 0
	sleep(2)
	echo("sleep 2s\n")
	GPIO.output( 22, 0)
	GPIO.output( 17, 0)
	GPIO.output( 14, 0)
	GPIO.output( 27, 0)
	sleep(0.5)

	#SERVER SETUP
	ip="192.168.78.233"
	port=80
	url ="http://{0}:{1}".format(ip,port)
	while True:
		try:

			inp = int(requests.get(url).text)

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

			if(inp == 2):
				if (motor_b_i <= 12):
					motor_b_i += 0.5
					motor_bas.ChangeDutyCycle(motor_b_i)
					time.sleep(1) 
			if(inp == 6):
				if (motor_b_i > 0.5):
					motor_b_i -= 0.5
					motor_bas.ChangeDutyCycle(motor_b_i)
					time.sleep(1) 
			if(inp == 8):
				if (motor_h_i > 0.5):
					motor_h_i -= 0.5
					motor_haut.ChangeDutyCycle(motor_h_i)
					time.sleep(1) 
			if(inp == 10):
				if (motor_h_i > 0.5):
					motor_h_i -= 0.5
					motor_haut.ChangeDutyCycle(motor_h_i) 
					time.sleep(1)
			
			motor_haut.ChangeDutyCycle(0)
			motor_bas.ChangeDutyCycle(0)
				
		except KeyboardInterrupt:
			GPIO.cleanup()
			motor_haut.stop()
			motor_bas.stop()
			return 0
		except:
			pass
	GPIO.cleanup()
	return 0

if __name__ == '__main__':
	sexit(main())
