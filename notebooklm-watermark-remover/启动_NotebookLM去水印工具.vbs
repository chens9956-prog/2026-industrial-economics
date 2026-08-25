Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strCurDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = strCurDir

pythonwPath = "C:\Users\ausu\AppData\Local\Programs\Python\Python312\pythonw.exe"
If fso.FileExists(pythonwPath) Then
    WshShell.Run """" & pythonwPath & """ """ & strCurDir & "\app.pyw""", 0, False
Else
    WshShell.Run "pyw -3.12 """ & strCurDir & "\app.pyw""", 0, False
End If
