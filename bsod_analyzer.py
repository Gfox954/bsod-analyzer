import json
import os
import subprocess
import time

# Folder where Windows stores minidumps
MINIDUMP_DIR = r"C:\Windows\Minidump"

def get_minidump_files():
    if not os.path.isdir(MINIDUMP_DIR):
        return []
    return [
        os.path.join(MINIDUMP_DIR, f)
        for f in os.listdir(MINIDUMP_DIR)
        if f.lower().endswith(".dmp")
    ]

def analyze_dump(dump_path):
    """
    Uses PowerShell + WinDbg (if installed) to get basic info.
    For now, we simulate analysis using 'strings' via PowerShell.
    This keeps it simple and still shows structure.
    """
    try:
        command = [
            "powershell",
            "-Command",
            f"Get-Content -Path '{dump_path}' -Encoding Byte -ReadCount 1024 | "
            "ForEach-Object { $_ } | "
            "Out-String"
        ]

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        raw_output = result.stdout

        # Very simple heuristic parsing (placeholder for real WinDbg integration)
        analysis = {
            "dump_path": dump_path,
            "bugcheck_code": "Unknown",
            "bugcheck_string": "Unknown",
            "faulting_driver": "Unknown",
            "notes": "Basic raw dump read completed. Integrate WinDbg for deeper analysis."
        }

        return analysis

    except Exception as e:
        return {
            "dump_path": dump_path,
            "error": str(e)
        }

def run_bsod_analyzer():
    dumps = get_minidump_files()

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "minidump_directory": MINIDUMP_DIR,
        "dump_count": len(dumps),
        "analysis": []
    }

    if not dumps:
        print("No minidump files found.")
    else:
        print(f"Found {len(dumps)} dump file(s). Analyzing...")

    for dump in dumps:
        print(f"Analyzing: {dump}")
        result = analyze_dump(dump)
        report["analysis"].append(result)

    with open("bsod_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("BSOD analysis complete. Report saved to bsod_report.json")

if __name__ == "__main__":
    run_bsod_analyzer()
