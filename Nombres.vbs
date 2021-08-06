Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c Nombres.bat"
oShell.Run strArgs, 0, flase