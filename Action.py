class Action(object):
	'''
	Convert events to actions
	'''
	def __init__(self):
		# direction mapping after rotation
		self.LEFT, self.RIGHT, self.DOWN, self.UP = 'down', 'up', 'right', 'left'
		self.actions = {
			'update_checkin': self._update_checkin,
			'prev_page': self._prev_page,
			'next_page': self._next_page,
			'prev_month': self._prev_month,
			'next_month': self._next_month,
			'reset': self._reset,
			'sleep': self._sleep,
		}


	def get_action(self, events):
		for action, action_func in self.actions.items():
			if action_func(events):
				return action
		return 'unknown'


	def _update_checkin(self, events):
		'''
		(un)checkin events
		single button press & release
		'''
		return len(events) == 2 and events[0].direction == 'middle'


	def _prev_page(self, events):
		'''
		switch to previous page
		single left press & release
		'''
		return len(events) == 2 and events[0].direction == self.LEFT


	def _next_page(self, events):
		'''
		switch to next page
		single right press & release
		'''
		return len(events) == 2 and events[0].direction == self.RIGHT

	
	def _prev_month(self, events):
		'''
		switch to the previous month
		single up press & release
		'''
		return len(events) == 2 and events[0].direction == self.UP


	def _next_month(self, events):
		'''
		switch to the next month
		single down press & release
		'''
		return len(events) == 2 and events[0].direction == self.DOWN


	def _reset(self, events):
		'''
		back to today
		long down press
		'''
		return len(events) > 10 and events[0].direction == self.DOWN


	def _sleep(self, events):
		'''
		turn on/off screen
		long press middle button
		'''
		return len(events) > 10 and events[0].direction == 'middle'
