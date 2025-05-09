import sys
import time

def wait_with_progress(seconds=120):
    print(f"⏳ Waiting {seconds} seconds for OSPF to converge...\n")
    for i in range(seconds):
        time.sleep(1)
        percent = int((i + 1) / seconds * 100)
        bar = '#' * (percent // 2)
        sys.stdout.write(f"\r🕒 {percent}% [{bar:<50}]")
        sys.stdout.flush()
    print("\n✅ OSPF wait complete.\n")
