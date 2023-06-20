
__all__ = [
	'LF',
	'clsLogger',
	'ConfigLog',
	'WriteLogArgs',
	'CloseLog'
	]


import pathlib
import io
import datetime
import sys


#-------------------------------------------------------------
# 
#-------------------------------------------------------------

LF = '\n'
C_CHR_None = '<None>'
C_NUM_None = -1
C_NEW_LINE = LF

#-------------------------------------------------------------
# 
#-------------------------------------------------------------

class clsLogger:
	
	logger_list = []
	
	PRN_SCREEN_AND_FILE = 1
	PRN_SCREEN_ONLY = 2
	PRN_FILE_ONLY = 3
	PRN_FLUSH_LOG_THRESHOLD = 100
	
	def __init__(self, prn_flag=1):
		
		_cls = clsLogger
		
		self.prn_flag = prn_flag
		self.log_cnt = 0
			
		self.logfilepath = self.get_default_log_path('.log')
			
		self.logbuf = io.StringIO()
			
		if self not in _cls.logger_list:
			_cls.logger_list.append(self)
			msg = 'Logger Starting. . .'
			with open(self.logfilepath,'w',encoding='utf-8') as f:
				f.write('')
				self.WriteLog(msg)
		else:
			raise Exception ('Logger already established')
			
	def get_default_log_path(self,extention='.log'):
			return str(pathlib.Path(__file__).stem + '_' + \
				datetime.datetime.now().strftime("%Y%m%d_%H%m%S%f") + extention)
				
			
	def WriteLog(self, arg):
		
		_cls = clsLogger
		
		if self.log_cnt >= _cls.PRN_FLUSH_LOG_THRESHOLD:
			self.FlushLog()
		
		arg_str = str(arg)
		if self.prn_flag == _cls.PRN_SCREEN_AND_FILE:
			self.logbuf.write(arg_str)
			sys.stdout.write(arg_str)
		elif self.prn_flag == _cls.PRN_SCREEN_ONLY:
			sys.stdout.write(arg_str)
		else:
			self.logbuf.write(arg_str)
		
	
	def WriteLogArgs(self, *args):
		for e, arg in enumerate(args,start=1):
			arg_str = str(arg)
			if e == 1:
				arg_str = ''.join([LF,arg_str])
			#arg_str = str(arg)
			self.WriteLog(arg_str)
			
	def FlushLog(self):
		with open(self.logfilepath,'a',encoding='utf-8') as f:
			f.write(self.logbuf.getvalue())
		self.log_cnt = 0

	def CloseLog(self):
		self.FlushLog()
		self.logbuf.close()
				
			
#-------------------------------------------------------------
# 
#-------------------------------------------------------------
		
def ConfigLog():
	# instantiate logger
	clsLogger()
	
		
def WriteLogArgs(*args):
	_cls = clsLogger
	_obj = _cls.logger_list[0]
	_obj.WriteLogArgs(*args)
	
def CloseLog():
	_cls = clsLogger
	_obj = _cls.logger_list[0]
	_obj.CloseLog()



#-------------------------------------------------------------
# 
#-------------------------------------------------------------




#-------------------------------------------------------------
# 
#-------------------------------------------------------------

def main():
	
	ConfigLog()
	WriteLogArgs(LF,__file__,' started.',LF)
	
	WriteLogArgs(LF,__file__,' completed.',LF)
	CloseLog()
	
if __name__ == '__main__':
	main()
