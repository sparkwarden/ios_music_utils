
#---------------------------------------------------------------------
#
#---------------------------------------------------------------------

__author__ = 'Gary D. Smith <https://github.com/sparkwarden>'
__version__ = '1.0'
__date__ = '2023/05/19'

#---------------------------------------------------------------------
# 
#---------------------------------------------------------------------


import pathlib
import subprocess


LF = '\n'

#-------------------------------------------------------------
# 
#-------------------------------------------------------------

def build_file_list(startdir:str=None, filterstr='*.*'):
	
	_file_list = []
	
	if startdir is None:
		_startdir = str(pathlib.Path().cwd())
	else:
		_startdir = startdir
	
	p = pathlib.Path(_startdir)
	
	glob_list = p.rglob(filterstr)
	
	for path in glob_list:
		_path = str(path)
		p = pathlib.Path(_path)
		
		if p.is_file(): 
			_file_list.append(_path)
			
	
	return _file_list

#-------------------------------------------------------------
# 
#-------------------------------------------------------------


def main():
	
	
	print(f'{LF} program {__file__} started.{LF}')
	
	curdir = str(pathlib.Path().cwd())
	
	
	file_list = build_file_list(startdir=curdir, filterstr='*.mp4')
	
	output_quality = str(input('Output Quality: [D]efault, [H]igh ')).upper()
	if output_quality in ['D','H']:
		
		for path in file_list:
			
			_from_path = str(path)
			
			_to_path = _from_path.rstrip('.mp4') + '.mp3'
			
			
			if output_quality == 'D':
				cmd_list = ['ffmpeg', '-i', _from_path, _to_path]
			else:
				cmd_list = ['ffmpeg', '-i', _from_path, \
				'-b:a', '320k', '-f', 'mp3', _to_path]
			
			completed = subprocess.run(cmd_list)
			print(f'{LF}returncode: {completed.returncode}')
		
		
	
	print(f'{LF} program {__file__} completed.{LF}')
	

	
if __name__ == '__main__':
	main()
