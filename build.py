import subprocess
import sys

def build():
    """PyInstallerでビルドを実行"""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        "--windowed",
        "--name", "AdobeGenuineService-DisableTool-v1.0",
        "--icon=favicon.ico",
        "main.py"
    ]
    
    try:
        print("building the application...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("successfully built the application.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("ビルド失敗:", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build()