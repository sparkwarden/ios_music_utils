#---------------------------------------------------------------------
#
#---------------------------------------------------------------------

__author__ = 'Gary D. Smith <https://github.com/sparkwarden>
__version__ = '1.0'
__date__ = '2023/05/19'

#---------------------------------------------------------------------
# 
#---------------------------------------------------------------------


from pytube_dl_lib import ConfigLog
from pytube_dl_lib import WriteLogArgs
from pytube_dl_lib import CloseLog
from pytube_dl_lib import LF


from pytube import Playlist
from pytube import YouTube


from pytube.exceptions import LiveStreamError
from pytube.exceptions import PytubeError
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import AgeRestrictedError
from pytube.exceptions import HTMLParseError


from pytube.exceptions import MaxRetriesExceeded
from pytube.exceptions import RecordingUnavailable
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoPrivate
from pytube.exceptions import VideoRegionBlocked
from pytube.exceptions import ExtractError


except_tuple = (LiveStreamError, PytubeError, VideoUnavailable,\
AgeRestrictedError, ExtractError, HTMLParseError, LiveStreamError,\
MaxRetriesExceeded,  PytubeError, RecordingUnavailable,\
RegexMatchError,VideoPrivate, VideoRegionBlocked, VideoUnavailable)

#--------------------------------------------------------------------
# 
#--------------------------------------------------------------------

import pathlib
import console
from dialogs import list_dialog


def input_prompt(prompt, skip=LF):
	WriteLogArgs(skip)
	retstr = input(prompt)
	WriteLogArgs(skip)
	return str(retstr)


def on_progress(stream, chunk, bytes_remaining):
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining
	percentage_of_completion = int(bytes_downloaded / total_size * 100)
	WriteLogArgs(f'{LF} {percentage_of_completion}% {LF}')


def make_YT_obj(url):
	yt_obj = None
	try:
		yt_obj = YouTube(url)
	except VideoUnavailable:
		raise Exception(f'Video {url} is unavaialable, skipping.')
	return yt_obj
	

def make_PL_obj(url):
	pl_obj = None
	try:
		pl_obj = Playlist(url)
	except (VideoUnavailable, PytubeError) as ex:
		raise Exception(f'playlist exception: {ex} .')
		pl_obj = None
	return pl_obj
	

def walk_recursive_data(rdata):
	
	if isinstance(rdata,list) or isinstance(rdata,tuple):
		for i in rdata:
			walk_recursive_data(i)
	elif isinstance(rdata,dict):
		for k,v in rdata.items():
			walk_recursive_data((k,v))
	else:
		WriteLogArgs(f'{LF} type: {rdata}')
			



def download_YT_file(url, yt_type='mp3'):
	
	
	if yt_type not in ['mp4', 'mp3', 'lst']:
		WriteLogArgs('Invalid Output Type: ', yt_type)
	else:
		yt = make_YT_obj(url)
		if yt:
			
			if yt_type == 'lst':
				WriteLogArgs(f'{LF}Logging {yt.title}. . .')
				msg = f'{LF} title: {yt.title} '
				msg += f'{LF} author: {yt.author} '
				msg += f'{LF} pubdate: {yt.publish_date} '
				msg += f'{LF} desc: {yt.description} '
				msg += f'{LF} '
				WriteLogArgs(msg)
			else:
				WriteLogArgs(f'{LF}Downloading title: {yt.title}. . .')
				
				try:
					yt.register_on_progress_callback(on_progress)
				
					try:
						if yt_type == 'mp3':
							outvid = yt.streams.filter(only_audio=True).first().download()
							try:
								outvid_ren = str(outvid).rstrip('.mp4') + '.mp3'
								p = pathlib.Path(outvid)
								p.rename(outvid_ren)
							
							except (OSError, Exception) as ex:
								raise Exception(ex)
							
						elif yt_type == 'mp4':
							yt.streams.filter(file_extension='mp4').first().download()
						
					except except_tuple as ex:
						WriteLogArgs(f'Download Stream Error {ex}:')
						
						
				except (VideoUnavailable, PytubeError) as ex:
						raise Exception(f'Download Prep Error {ex}:')
				
				WriteLogArgs(f'{LF}Download of {yt.title} completed.')
			
				

def input_loop():
	
	while True:
		console.clear()
		WriteLogArgs('')
		
		yt_type_list = ['Playlist', 'URL']
		ld1 = 'Enter Type'
		ld2 = False
		ld3 = yt_type_list
		yt_type = list_dialog(title=ld1, multiple=ld2, items=ld3)
		
		if (yt_type == '') or (yt_type is None):
			break
		
		video_ext_list = ['mp4', 'mp3', 'lst']
		
		ld1 = 'Output File Ext'
		ld2 = False
		ld3 = video_ext_list
		
		yt_out_type = list_dialog(title=ld1, multiple=ld2, items=ld3)
		
		if yt_out_type == '' or yt_out_type is None:
			break
		
		if yt_type == 'URL':
			url = input_prompt('Enter Video URL:')
			if url != '':
				download_YT_file(url, yt_type=yt_out_type)
				
		elif yt_type == 'Playlist':
			playurl = input_prompt('Enter PlayList URL:')
			if playurl != '':
				
				plobj = Playlist(playurl)
				
				_title = plobj.title
				WriteLogArgs(f'{LF} title: {_title}')
				#_sidebar_info = plobj.sidebar_info
				#walk_recursive_data(_sidebar_info)
				
				for url in plobj:
					download_YT_file(url, yt_type=yt_out_type)

#--------------------------------------------------------------------
# 
#--------------------------------------------------------------------

def main():
	
	ConfigLog()
	WriteLogArgs(LF, __file__, ' started.', LF)
	
	input_loop()
	WriteLogArgs(LF, __file__, ' completed.', LF)
	CloseLog()
	
if __name__ == '__main__':
	main()
