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

from mutagen.id3 import ID3NoHeaderError
	
from mutagen.id3 import ID3, TIT2, TALB, TPE1, \
	TPE2, COMM, TCOM, TCON, TDRC, TRCK

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




def tags_get_file(fname):
	try:
		tags = ID3(fname)
	except ID3NoHeaderError:
		print("No ID3 header")
		tags = None
		
	return tags
	


def tag_file(fname, title, trackno, album, artist, genre, relyear):
		
	tags = ID3()

	tags["TIT2"] = TIT2(encoding=3, text=title)
	tags["TALB"] = TALB(encoding=3, text=album)
	tags["TPE2"] = TPE2(encoding=3, text='')
	tags["COMM"] = COMM(encoding=3, lang=u'eng', desc='desc', text='')
	tags["TPE1"] = TPE1(encoding=3, text=artist)
	tags["TCOM"] = TCOM(encoding=3, text=artist)
	tags["TCON"] = TCON(encoding=3, text=genre)
	tags["TDRC"] = TDRC(encoding=3, text=relyear)
	tags["TRCK"] = TRCK(encoding=3, text=trackno)
	
	tags.save(fname)




def show_files(update_tags=True):
	
	curdir = str(pathlib.Path.cwd())
	mp3_file_list = build_file_list(curdir,'*.mp3')
	
	for path in mp3_file_list:
			
			
			_path = str(path)
			
			p = pathlib.Path(_path)
			_parts = list(p.parts)
			
		
			title_split = str(p.name).split(' - ')
			
			_title = str(title_split[1]).replace('.mp3','')
			_trackno = title_split[0]
			
			l = len(_parts)
			#_filepart = _parts[l-1]
			_albumpart = str(_parts[l-2])
			_artist = str(_parts[l-3])
			_genre = str(_parts[l-4])
			
			if _albumpart.find('-') > 0:
				_albumsplit = _albumpart.split('-')
				_album = _albumsplit[0]
				_relyear = _albumsplit[1]
			else:
				_album = _albumpart
				_relyear = ''
			
			print(f'{LF}path: {path}')
			print(f'{LF}trackno: {_trackno}')
			print(f'{LF}title: {_title}')
			#print(f'{LF}parts: {_parts}')
			print(f'{LF}artist: {_artist}')
			print(f'{LF}album: {_album}')
			print(f'{LF}relyear: {_relyear}')
			
			
			if update_tags:
				tag_file(_path, _title, _trackno, _album, _artist, _genre, _relyear)
			
			
			

	

def main():
	''' Main Program. '''
	
	
	
	print(f'{LF}*** program {__file__} started. ***')
	
	show_files(update_tags=True)
	
	
	
	
			
	print(f'{LF}*** program {__file__} completed. ***')

	
	
	
	
	
	

#---------------------------------------------------------------------
#
#---------------------------------------------------------------------

if __name__ == '__main__':
	main()
	
	



		
