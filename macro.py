import threading
import time

import evdev
from evdev import InputDevice, UInput, ecodes

# --- CONFIG MACRO ---
KEY_TO_PRESS = ecodes.KEY_D  # The key to be used
TOGGLE_KEY = ecodes.KEY_INSERT  # Toggle ON/OFF
DELAY = 0.5  # Delay
# -------------------------

is_running = False
ui = UInput()


def find_keyboard():
    """Auto find physical keyboard"""
    devices = [InputDevice(path) for path in evdev.list_devices()]
    keyboards = []
    for dev in devices:
        caps = dev.capabilities()
        if ecodes.EV_KEY in caps and ecodes.KEY_A in caps[ecodes.EV_KEY]:
            keyboards.append(dev)
    return keyboards


def macro_loop():
    """Background process for executing automated typing."""
    global is_running
    while True:
        if is_running:
            ui.write(ecodes.EV_KEY, KEY_TO_PRESS, 1)  # press
            ui.write(ecodes.EV_KEY, KEY_TO_PRESS, 0)  # release
            ui.syn()
            time.sleep(DELAY)
        else:
            time.sleep(0.5)


def listen_device(dev):
    """Capture keyboard events from one device."""
    global is_running
    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:  # 1 = key down
                if event.code == TOGGLE_KEY:
                    is_running = not is_running
                    status = "ON (ACTIVE)" if is_running else "OFF (INACTIVE)"
                    print(f"[{time.strftime('%H:%M:%S')}] Status Macro: {status}")
    except OSError:
        pass


def main():
    print("=============================================")
    print("   ARCH LINUX (HYPRLAND) AUTO KEYBOARD MACRO  ")
    print("   (versi evdev - kompatibel Wayland)         ")
    print("=============================================")
    print(f" Tombol Macro   : '{ecodes.KEY[KEY_TO_PRESS]}'")
    print(f" Toggle ON/OFF  : [{ecodes.KEY[TOGGLE_KEY]}]")
    print(f" Delay Interval : {DELAY} detik")
    print("=============================================")

    keyboards = find_keyboard()
    if not keyboards:
        print("ERROR: Tidak ada keyboard terdeteksi di /dev/input/.")
        print("Pastikan user sudah masuk grup 'input' lalu logout/login ulang.")
        return

    print("Keyboard terdeteksi:")
    for kb in keyboards:
        print(f"  - {kb.path} ({kb.name})")
    print("=============================================")
    print("Tekan Ctrl+C di terminal untuk menghentikan program.\n")

    macro_thread = threading.Thread(target=macro_loop, daemon=True)
    macro_thread.start()

    #
    listener_threads = []
    for kb in keyboards:
        t = threading.Thread(target=listen_device, args=(kb,), daemon=True)
        t.start()
        listener_threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram macro dihentikan.")


if __name__ == "__main__":
    main()
