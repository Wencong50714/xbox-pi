import asyncio
import sys
from evdev import InputDevice, ecodes, ff, list_devices
import gamepad

def connect(): # asyncronus read-out of events
        xbox_path = None
        remote_control = None
        devices = [InputDevice(path) for path in list_devices()]
        print('Connecting to xbox controller...')
        for device in devices:
            if str.lower(device.name) == 'xbox wireless controller':
                xbox_path = str(device.path)
                remote_control = gamepad.gamepad(file = xbox_path)
                remote_control.rumble_effect = 2
                print("find xbox wireless controller")
                return remote_control
        return None

def is_connected(): # asyncronus read-out of events
    path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            path = str(device.path)
    if(path == None):
        print('Xbox controller disconnected!!')
        return False
    return True


async def main():
    try:
        remote_control = connect()
        if(remote_control == None):
            print('Please connect an Xbox controller then restart the program!')
            sys.exit() 

        while True:
            tasks = [
                asyncio.create_task(remote_control.read_gamepad_input()),
                asyncio.create_task(remote_control.rumble()),
            ]
            await asyncio.gather(*tasks)
    except Exception as e:
        print("Error occured " + str(e))
    finally:
        if remote_control != None:
            remote_control.power_on = False
            remote_control.erase_rumble()

        print("Done..")

if __name__ == "__main__":
    asyncio.run(main())