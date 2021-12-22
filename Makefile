output: clean
	-echo "building..."
	-pyinstaller.exe --icon=tomato.ico -n=Pomodoro --onefile .\main.pyw
clean:
	-echo "cleaning..."
	-rm dist
