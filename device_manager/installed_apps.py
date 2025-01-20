import subprocess
from functools import lru_cache
from typing import List


@lru_cache(maxsize=20)
def get_installed_apps(device_id: str) -> List[str]:
    """Fetches a list of all installed applications on the specified Android device."""
    try:
        adb_command = ["adb"]
        if device_id:
            adb_command.extend(["-s", device_id])

        # Add the shell command to list packages
        adb_command.extend(["shell", "pm", "list", "packages"])

        result = subprocess.run(
            adb_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"Error fetching installed apps for device '{device_id}': {result.stderr}")
            return []

        # Extract package names from the result
        packages = [line.split(":")[1] for line in result.stdout.strip().splitlines()]
        return packages

    except Exception as e:
        print(f"Error: {e}")
        return []


def find_app_by_name(application_name: str, device_id: str) -> str | None:
    """Checks if the specified app is installed on the device and returns its package name."""
    app_name_lower = application_name.lower()
    installed_apps = get_installed_apps(device_id=device_id)

    exact_matches = []
    partial_matches = []

    for package in installed_apps:
        if app_name_lower == package.split('.')[-1].lower():
            exact_matches.append(package)

        elif app_name_lower in package.lower():
            partial_matches.append(package)

    if exact_matches:
        return exact_matches[0]  # Return the first exact match

    elif partial_matches:
        return partial_matches[0]  # Return the first partial match

    return None

