from .cli import serv
from .cli import start
from .cli import chapter
from .cli import select
from .cli import downdir
from .cli import finish

def main():
	serv()
	start()
	chapter()
	select()
	downdir()
	finish()
if __name__ == "__main__":
	main()