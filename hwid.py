import subprocess

def get_hwid():
    try:
        # Run the 'wmic' command to get hardware information
        result = subprocess.check_output(['wmic', 'csproduct', 'get', 'uuid']).decode('utf-8')
        # Extract the HWID from the result
        hwid = result.split('\n')[1].strip()
        return hwid
    except Exception as e:
        print(f"Error getting HWID: {e}")
        return None

# Example usage
hwid = get_hwid()
if hwid:
    print(f"Hardware ID (HWID): {hwid}")
else:
    print("Failed to retrieve HWID.")
