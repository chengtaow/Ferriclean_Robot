import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
import random

class Ferriclean:
	def __init__(self):
		#init signal for motor dirction
		GPIO.setup("P8_7", GPIO.OUT)
		GPIO.setup("P8_8", GPIO.OUT)
		GPIO.setup("P8_9", GPIO.OUT)
		GPIO.setup("P8_10", GPIO.OUT)
		#init signal for left, right brush
		GPIO.setup("P8_17", GPIO.OUT)
		GPIO.setup("P8_18", GPIO.OUT)
		#init signal for left, right encoder
		GPIO.setup("P9_15", GPIO.IN)
		GPIO.setup("P9_21", GPIO.IN)
		#set up ADC for IR sensor
		ADC.setup()
		self.mid = ADC.read("P9_35")
        	self.lef = ADC.read("P9_33")
       		self.rig = ADC.read("P9_36")	
		self.mrig = ADC.read("P9_40")
		self.mlef = ADC.read("P9_39")
		self.value = [self.lef, self.mid, self.rig, self.mlef, self.mrig]

		#set up the interrupt of encoder
		GPIO.add_event_detect("P9_15", GPIO.BOTH, callback = encoder_right)
		GPIO.add_event_detect("P9_21", GPIO.BOTH, callback = encoder_left)

		self.direction_right = True
		self.direction_left = True
		self.distance_right = 0
		self.distance_left = 0
		self.direction_angle = 0
		self.__spd = 20
		self.__spd1 = 38
		self.__spd2 = 38

	def __leftf(forward):
		# The left wheel go forward
		PWM.start("P8_13", forward, 50, 0)
		GPIO.output("P8_7", GPIO.LOW)
		GPIO.output("P8_8", GPIO.HIGH)
	def __leftb(back):
		# The left wheel go back
		PWM.start("P8_13", back, 50, 0)
		GPIO.output("P8_7", GPIO.HIGH)
		GPIO.output("P8_8", GPIO.LOW)
	def __rigf(forward):
		# The right wheel go forward
		PWM.start("P9_14", forward, 50, 0)
		GPIO.output("P8_9", GPIO.HIGH)
        	GPIO.output("P8_10", GPIO.LOW)
	def __rigb(back):
		# The right wheel go back
		PWM.start("P9_14", back, 50, 0)
		GPIO.output("P8_9", GPIO.LOW)
        	GPIO.output("P8_10", GPIO.HIGH)

	def goforward(speed1, speed2):
		# The robot go forward
		self.direction_right = True
		self.direction_left = True
		__leftf(speed1)
		__rigf(speed2)

	def goback(speed1, speed2):
		# The robot go back
		self.direction_right = False
		self.direction_left = False
		__leftb(speed1)
		__rigb(speed2)

	def turnrig():
		# The robot turn right
		self.direction_right = False
		self.direction_left = True
		__leftf(self.__spd)
		__rigb(self.__spd)

	def turnleft():
		# The robot turn left
		self.direction_right = True
		self.direction_left = False
		__leftb(self.__spd)
		__rigf(self.__spd)

	def stop():
		# The robot stop
		__leftb(0)
		__rigb(0)

#	def brush(brush_left, brush_right):
#		if brush_left == True:
#			GPIO.output("P8_17", GPIO.HIGH)
#		else:
#			GPIO.output("P8_17", GPIO.LOW)
#		if brush_right == True:
#			GPIO.output("P8_18", GPIO.HIGH)
#		else:
#			GPIO.output("P8_18", GPIO.LOW)

	def encoder_right(channel):
		# The call back function for right encoder
		if self.direction_right == True:
			self.distance_right += 1
		if self.direction_right == False:
			self.distance_right -= 1

	def encoder_left(channel):
		# The call back function for left encoder
		if self.direction_left == True:
			self.distance_left += 1
		if self.direction_left == False:
			self.distance_left -= 1

	def obstacle_avoidance():
		while True:
			if self.lef > 0.35 and self.rig < 0.35:
				turnrig()
			elif self.rig > 0.35 and self.lef < 0.35:
				turnleft()
			elif self.lef > 0.3 and self.rig > 0.3 or self.mid > 0.3:
				ranturn = random.randint(1,4)
				if ranturn > 2:
					turnrig()
				else:
					turnleft()
				time.sleep(1)
			else:
				goforward(self.spd, self.spd)
			print self.distance_left, self.distance_right
			time.sleep(0.1)

	def brushcontrol():
		while True:
			if self.mlef > 0.4:
				GPIO.output("P8_17", GPIO.HIGH)
			else:
				GPIO.output("P8_17", GPIO.LOW)
			if self.mrig > 0.4:
				GPIO.output("P8_18", GPIO.HIGH)
			else:
				GPIO.output("P8_18", GPIO.LOW)
			time.sleep(0.1)

	def __del__(self):
		GPIO.cleanup()
		PWM.stop("P8_13")
		PWM.stop("P9_14")
		PWM.cleanup()
		print 'Good Bye!'



















