import pandas as pd
from datetime import date
from calendar import monthrange
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Record(object):
	'''
	Manage record file
	'''
	def __init__(self, recordfile):
		self.file = recordfile
		self.record_df = None
		self.last_col = 0

		self.acts = []
		self.act_num = 0

		self.dateobj = date.today()
		
		self.load_file()
		self.update_df()
		self.save_df()


	def update_date(self, how):
		'''
		Update the dateobj and also YMD
		Support three methods
		Return: is_cur_month (bool)
		'''
		if how == 'reset':
			is_cur_month = True
			self.dateobj = date.today()
			
		elif how == 'prev':
			is_cur_month = False
			self.dateobj = self.dateobj - relativedelta(months=1)

		elif how == 'next':
			self.dateobj = self.dateobj + relativedelta(months=1)
			if self.dateobj >= date.today():
				is_cur_month = True
				self.dateobj = date.today()
			else:
				is_cur_month = False
		
		elif how == 'no':
			if self.dateobj.month == date.today().month:
				self.dateobj = date.today()
				is_cur_month = True
			else:
				is_cur_month = False
		else:
			raise Exception('Method {} is not supported'.format(how))

		return is_cur_month


	def load_file(self):
		'''
		Load record file, update the parameters
		'''
		self.record_df = pd.read_csv(self.file)
		self.last_col = len(self.record_df['year']) - 1

		self.acts = [a for a in self.record_df.columns][3:]
		self.act_num = len(self.acts)


	def save_df(self):
		'''
		Update the record file with the crrent record df
		'''
		self.record_df.to_csv(self.file, index = None)


	def update_df(self):
		'''
		Fill all the past days records
		Need to be called everytime when updating the status matrix
		'''
		prev_y, prev_m, prev_d = self.record_df['year'][self.last_col], self.record_df['month'][self.last_col], self.record_df['day'][self.last_col]
		prev_date = date(prev_y, prev_m, prev_d)
		cur_date = date.today()

		while prev_date < cur_date:
			prev_date = prev_date + timedelta(days = 1)
			self.last_col += 1
			self.record_df.loc[self.last_col] = [prev_date.year, prev_date.month, prev_date.day] + [0 for _ in self.acts]


	def flip_cur_status(self, activity, status):
		'''
		Check / Uncheck the current status
		Save the status to file
		'''
		self.record_df.loc[self.last_col][activity] = status
		self.save_df()


	def get_cur_status_matrix(self, activity):
		'''
		Convert df to matrix
		Return: (matrix, cur day, last day in cur month)
		'''
		self.update_df()
		y, m, d = self.dateobj.year, self.dateobj.month, self.dateobj.day
		cr_df = self.record_df[self.record_df['year'] == y][self.record_df['month'] == m]
		matrix = list(cr_df[activity])
		matrix += [0 for _ in range(5*8 - len(matrix))]

		last_day = monthrange(y, m)[-1]
		return matrix, d, last_day


	def get_month_matrix(self):
		'''
		Get the matrix to represent month [1, 12]
		Input: month
		Return: 1*24 month matrix (flatten 3*8 matrix)
		'''
		month = self.dateobj.month

		month_matrix = [[0 for _ in xrange(8)] for _ in range(3)]
		if month >= 10:
			month_matrix[0][0] = 1
			digit = month - 10
		else:
			digit = month

		row = int(digit / 3)
		remain = digit % 3

		for i in range(row):
			for j in range(2, 5):
				month_matrix[i][j] = 1

		if remain:
			for j in range(remain):
				month_matrix[row][j+2] = 1

		flatten = lambda l: [item for sublist in l for item in sublist]
		return flatten(month_matrix)


