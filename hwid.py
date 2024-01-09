import subprocess

def get_hwid():
    try:
        result = subprocess.check_output(['wmic', 'csproduct', 'get', 'uuid']).decode('utf-8')
        hwid = result.split('\n')[1].strip()
        return hwid
    except Exception as e:
        print(f"Error getting HWID: {e}")
        return None


hwid = get_hwid()
if hwid:
    print(f"Hardware ID (HWID): {hwid}")
else:
    print("Failed to retrieve HWID.")
