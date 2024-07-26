PyV=python3
Setup_Files=setup.py
Main_Files=main.py
Delete_Files=build calculator.egg-info dist
all: setup main

setup:
	$(PyV) $(Setup_Files) install

run:
	python3 main.py

clean:
	rm -rf $(Delete_Files)