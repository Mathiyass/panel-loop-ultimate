import os
import subprocess
import winreg

print("=== 1. VERIFYING RUNNING PROCESSES ===")
out = subprocess.check_output("tasklist /FO CSV /NH", text=True)
procs = [l for l in out.splitlines() if any(t in l.lower() for t in ["emulator", "aow", "tencent", "appmarket", "txgame"])]
print("Active GameLoop processes:", procs if procs else "NONE (Clean)")

print("\n=== 2. VERIFYING SERVICES & DRIVERS ===")
for s in ["QMEmulatorService", "aow_drv"]:
    res = subprocess.run(["sc", "query", s], capture_output=True, text=True)
    status = "NOT FOUND (Clean)" if ("1060" in res.stdout or "1060" in res.stderr or "FAILED" in res.stdout) else res.stdout.strip()
    print(f"Service/Driver {s}: {status}")

print("\n=== 3. VERIFYING SCHEDULED TASKS ===")
res = subprocess.run(["schtasks", "/query", "/tn", r"\RunGameLoopInstaller"], capture_output=True, text=True)
task_status = "NOT FOUND (Clean)" if ("ERROR" in res.stderr or "cannot find" in res.stderr.lower()) else "STILL EXISTS"
print(f"Scheduled Task \\RunGameLoopInstaller: {task_status}")

print("\n=== 4. VERIFYING TARGET DIRECTORIES ===")
target_dirs = [
    r"C:\Program Files\TxGameAssistant",
    r"C:\GameLoopSetup",
    r"C:\Temp\TxGameDownload",
    r"C:\Program Files (x86)\GameLoopHub",
    r"C:\Windows\Temp\Tencent",
    r"C:\ProgramData\Tencent",
    r"C:\Users\MATHIYA\AppData\Roaming\Tencent",
    r"C:\Users\MATHIYA\AppData\Local\Tencent"
]
for d in target_dirs:
    exists = os.path.exists(d)
    print(f"Directory {d}: {'STILL EXISTS' if exists else 'DELETED (Clean)'}")

print("\n=== 5. VERIFYING SHORTCUTS ===")
sc = r"C:\Users\MATHIYA\Desktop\AndroidEmulator - Shortcut.lnk"
print(f"Shortcut {sc}: {'STILL EXISTS' if os.path.exists(sc) else 'DELETED (Clean)'}")

print("\n=== 6. VERIFYING REGISTRY HIVES ===")
for root, rname, sub in [
    (winreg.HKEY_CURRENT_USER, "HKCU", r"Software\Tencent"),
    (winreg.HKEY_LOCAL_MACHINE, "HKLM", r"SOFTWARE\WOW6432Node\Tencent"),
    (winreg.HKEY_LOCAL_MACHINE, "HKLM", r"SOFTWARE\Tencent"),
    (winreg.HKEY_USERS, "HKU", "QMConfig")
]:
    try:
        k = winreg.OpenKey(root, sub)
        winreg.CloseKey(k)
        print(f"Registry {rname}\\{sub}: STILL EXISTS")
    except OSError:
        print(f"Registry {rname}\\{sub}: NOT FOUND (Clean)")

print("\n=== 7. VERIFYING FIREWALL RULES ===")
res = subprocess.run(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"], capture_output=True, text=True, errors="ignore")
gl_rules = [l for l in res.stdout.splitlines() if any(x in l.lower() for x in ["androidemulator", "appmarket", "txgame"])]
print("Firewall rules remaining:", len(gl_rules))

print("\n=== 8. VERIFYING PROTECTED DIRECTORIES ===")
p1 = r"C:\Program Files\TAC Panel Loop"
p2 = r"C:\Users\MATHIYA\Documents\saasassasa"
print(f"Protected {p1}: {'PRESERVED (OK)' if os.path.exists(p1) else 'MISSING!'}")
print(f"Protected {p2}: {'PRESERVED (OK)' if os.path.exists(p2) else 'MISSING!'}")
