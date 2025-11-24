import subprocess
import ctypes
import time

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

script_path = "code/face_classifier_ready.py"

for i in range(1000):
    print(f"Запуск {i + 1}")
    subprocess.run(["python", script_path, "--no-show"])

ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
