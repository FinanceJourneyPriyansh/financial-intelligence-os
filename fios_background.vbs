Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = "C:\Github\financial-intelligence-os"
shell.Run """C:\Github\financial-intelligence-os\.venv\Scripts\python.exe"" ""C:\Github\financial-intelligence-os\main.py""", 0, True
