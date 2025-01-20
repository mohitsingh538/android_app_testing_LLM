import time
from typing import Any
import streamlit as st
from device_manager.connected_devices import get_all_devices_info
from device_manager.installed_apps import find_app_by_name
from llm.function_calling import action_handlers
from utils.appium_manager import AppiumAppManager
from llm.parser import LLMAutomation


def main():
    st.title("Debug Playground")

    # Input for app name
    app_name = st.text_input("Enter App Name:", value="Zepto")

    # Get connected devices
    devices = get_all_devices_info()

    if not devices:
        st.error("No devices connected for Debugging")
        return

    # Create device selection dropdown
    device_options = ["All Devices"] + [f"{device.device_name} ({device.device_id})" for device in devices]
    selected_device = st.selectbox("Select Device:", device_options)

    # Instructions input
    instructions_text = st.text_area(
        "Enter Instructions (one per line):",
        value="Open the app\nWait for the home screen to load\nTake a screenshot\nSearch for 'Chocolates'",
        height=200
    )

    # Convert instructions text to list
    instructions = [line.strip() for line in instructions_text.split('\n') if line.strip()]

    # Debug button
    if st.button("Debug"):
        # Create a status container
        status = st.empty()

        if selected_device == "All Devices":
            # Run on all devices
            for device in devices:
                run_debug_for_device(device, app_name, instructions, status)
        else:
            # Run on selected device
            selected_device_id = selected_device.split('(')[-1].rstrip(')')
            selected_device_obj = next((d for d in devices if d.device_id == selected_device_id), None)
            if selected_device_obj:
                run_debug_for_device(selected_device_obj, app_name, instructions, status)


def run_debug_for_device(device, app_name: str, instructions: list, status: Any):
    """Run debug process for a specific device"""
    status.info(f"📱 Running on device: {device.device_id}")

    package_name = find_app_by_name(app_name, device_id=device.device_id)
    if not package_name:
        status.error(f"{app_name} is probably not installed on {device.device_name}")
        return

    manager = AppiumAppManager(
        app_package=package_name,
        app_activity=".MainActivity",
        device_id=device.device_id,
        platform_version=device.platform_version
    )

    try:
        manager.manage_state()

        # Create columns for progress and status
        progress_bar = st.progress(0)

        for idx, instruction in enumerate(instructions):
            # Update progress
            progress = (idx + 1) / len(instructions)
            progress_bar.progress(progress)

            status.info(f"Executing instruction: {instruction}")

            action = LLMAutomation.call_llm(instruction)
            if action:
                action_type = action.get("name")
                action_args = action.get("arguments")

                handler = action_handlers.get(action_type)
                if handler:
                    status.info(f"Executing action type: {action_type}")
                    handler.function(manager).execute(**action_args)

                else:
                    status.warning(f"No handler defined for action type: {action_type}")
            else:
                status.error("Failed to detect home screen.")

            # Add a small delay to make the progress visible
            time.sleep(0.5)

        status.success("Debug process completed successfully!")

    except Exception as e:
        status.error(f"Error during debug process: {str(e)}")

    finally:
        manager.quit()


if __name__ == "__main__":
    main()