$path = 'HKCU:\Software\Tencent\MobileGamePC'
if (-not (Test-Path $path)) {
    New-Item -Path $path -Force | Out-Null
}

$props = @{
    'VMPhoneDevice' = 'Asus ROG 8 Pro'
    'VMDeviceModel' = 'ASUS_AI2401_A'
    'VMDeviceManufacturer' = 'asus'
    'GraphicsCard' = 'Nvidia'
}

foreach ($item in $props.GetEnumerator()) {
    Set-ItemProperty -Path $path -Name $item.Key -Value $item.Value -Type String
}

$dwordProps = @{
    'com.tencent.ig_FPSLevel' = 120
    'VSyncEnabled' = 0
    'ForceDirectX' = 1
    'GraphicsCardEnabled' = 1
    'SetGraphicsCard' = 1
    'LocalShaderCacheEnabled' = 1
    'ShaderCacheEnabled' = 1
    'RenderOptimizeEnabled' = 1
    'EnableGLESv3' = 1
    'VMCpuCount' = 8
    'VMMemorySizeInMB' = 4096
    'VMResWidth' = 1920
    'VMResHeight' = 1080
    'VMDPI' = 480
    'FxaaQuality' = 0
}

foreach ($item in $dwordProps.GetEnumerator()) {
    Set-ItemProperty -Path $path -Name $item.Key -Value $item.Value -Type DWord
}

$ifeoPath = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AndroidEmulatorEx.exe\PerfOptions'
if (-not (Test-Path $ifeoPath)) {
    New-Item -Path $ifeoPath -Force | Out-Null
}
Set-ItemProperty -Path $ifeoPath -Name 'CpuPriorityClass' -Value 3 -Type DWord

Write-Output 'Registry optimizations applied successfully.'
