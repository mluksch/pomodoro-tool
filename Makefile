output: clean
	-echo "building..."
	-pyinstaller.exe --icon=tomato.ico --onefile .\main.pyw
clean:
	-echo "cleaning..."
	-rm dist
