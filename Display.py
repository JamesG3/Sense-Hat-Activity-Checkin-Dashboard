from sense_hat import SenseHat
import time
import settings

s = SenseHat()
s.low_light = True
s.set_rotation(270)

BLINK_TIME = 0.5


class Display(object):
	'''
	Display related functions
	'''
	def __init__(self):
		pass

	def show_msg(self, msg, color=settings.WHITE):
		s.show_message(msg, text_colour=color)
		

	def display_status(self, status):
		'''
		Display the give 1*64 (flatten 8x8 matrix) with RGB color
		Input: 1x64 RGB color matrix
		Return: None 
		'''
		s.set_pixels(status)


	def blink(self, status1, status2, blink_time=BLINK_TIME):
		'''
		Give two different 8x8 Matrix, blink once from status1 to status2
		If need to keep blinking, a while loop need to be set outside this func
		Input: Two different color matrices
		Return: None
		'''
		self.display_status(status1)
		time.sleep(blink_time)
		self.display_status(status2)
		time.sleep(blink_time)
