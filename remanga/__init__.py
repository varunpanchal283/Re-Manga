from .mangadex import (data, chapter, downloader)
from .manganelo import (data, chapter, downloader)
from .funmanga import (data, chapter, downloader)
from . import cli
__all__ = [
	'funmanga.data',
	'funmanga.chapter',
	'funmanga.downloader',
    'mangadex.data',
    'mangadex.chapter',
    'mangadex.downloader',
    'manganelo.data',
    'manganelo.chapter',
    'manganelo.downloader'
]