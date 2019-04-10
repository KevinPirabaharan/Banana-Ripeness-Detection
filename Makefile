all: main dependencies

dependencies: src/imageIO.py src/imthr_lib.py
	chmod u+x src/imageIO.py
	chmod u+x src/imthr_lib.py 

main: src/main.py
	chmod u+x src/main.py

clean:
	rm src/*.pyc
	rm src/*.jpeg

