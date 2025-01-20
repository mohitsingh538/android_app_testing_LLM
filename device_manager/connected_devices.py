import subprocess
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class DeviceInfo:
    device_name: str
    platform_version: str
    device_id: str

    def __str__(self):
        return f"DeviceInfo(device_name={self.device_name}, platform_version={self.platform_version}, device_id={self.device_id})"



def get_connected_devices():
    """
    Get a list of all connected Android devices.
    """
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")[1:]  # Skipping the first line (header)
        identified_devices = [line.split()[0] for line in lines if "device" in line]

        return identified_devices

    except subprocess.CalledProcessError as e:
        print("Error executing adb command:", e)
        return []


@lru_cache(maxsize=5)
def get_device_info(device_identifier):
    """
    Get device name and platform version for a given device ID.
    """
    try:
        device_name = subprocess.run(
            ["adb", "-s", device_identifier, "shell", "getprop", "ro.product.model"],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        platform_version = subprocess.run(
            ["adb", "-s", device_identifier, "shell", "getprop", "ro.build.version.release"],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        return DeviceInfo(device_name, platform_version, device_identifier)

    except subprocess.CalledProcessError as e:
        print(f"Error fetching details for device {device_identifier}:", e)
        return {"device_name": None, "platform_version": None}


def get_all_devices_info():
    identified_devices = get_connected_devices()
    if not identified_devices:
        print("No devices connected.")
        return

    device_info_list = []
    for device_identifier in identified_devices:
        device_info = get_device_info(device_identifier)
        device_info_list.append(device_info)

    return device_info_list