import subprocess

cmd = [
    'powershell',
    '-NoProfile',
    '-Command',
    "Get-WinEvent -FilterHashtable @{LogName='Application'; StartTime=(Get-Date).AddMinutes(-15)} -ErrorAction SilentlyContinue | Select-Object TimeCreated, Id, ProviderName, Message | Format-List"
]
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout[:2000] if res.stdout else "No events found.")
if res.stderr:
    print("Stderr:", res.stderr)
