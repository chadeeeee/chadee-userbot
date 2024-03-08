import os
import pathlib
from pathlib import Path

_file_path_ = os.path.abspath(__file__)
_HOME_DIR_ = os.environ.get('HOME')

_prefix_dir_= os.path.dirname(os.path.dirname('PREFIX'))
_ROOT_DIR_ = os.environ.get(_prefix_dir_) if 'PREFIX' in os.environ else '/'
_BOT_DIR_ = os.path.dirname(os.path.dirname(_file_path_))
_MAIN_FILE_ = 'main.py'

_JSON_DIR_ = str(Path(_BOT_DIR_, 'json')) + '/'
_YTDLP_DIR_ = str(Path(_BOT_DIR_, 'ytdlp_down')) + '/'
_DOWNLOADS_ =  str(Path(_BOT_DIR_, 'downloads')) + '/'

