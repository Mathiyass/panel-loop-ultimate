$sh = New-Object -ComObject WScript.Shell
$sc = $sh.CreateShortcut('C:\Users\MATHIYA\Desktop\AndroidEmulatorEx - Shortcut.lnk')
Write-Output "TargetPath: $($sc.TargetPath)"
Write-Output "Arguments: $($sc.Arguments)"
Write-Output "WorkingDirectory: $($sc.WorkingDirectory)"
