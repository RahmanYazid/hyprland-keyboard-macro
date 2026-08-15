# Arch Linux (Hyprland) Auto Keyboard Macro

A simple Python script for automating repeated key presses (auto-key macro), with an ON/OFF toggle triggered by a physical key. Built specifically to work on **Wayland/Hyprland**, using `evdev` instead of `pynput`, since `pynput` cannot detect or simulate input globally on Wayland compositors.

## Features

- Automatically repeats a chosen key press with a configurable delay
- Toggle ON/OFF using a physical key (default: `Insert`)
- Auto-detects connected physical keyboards
- Compatible with Hyprland and other Wayland compositors (not blocked by the global-input restrictions that affect `pynput`)

## Requirements

- Arch Linux (or any other Linux distro) with Hyprland / a Wayland compositor
- Python 3.10+
- Access to `/dev/uinput` and `/dev/input/eventX` (via membership in the `input` group)
- Python package: `evdev`

## Project Structure

```
macropython/
├── macro.py            # Main script
├── README.md            # This documentation
├── requirements.txt      # Python dependency list
└── .gitignore            # Ignores venv/ and cache files
```

## Installation

### 1. Clone the repository

```bash
# HTTPS
git clone https://github.com/RahmanYazid/hyprland-keyboard-macro.git

# or via SSH (requires SSH key already set up on your GitHub account)
git clone git@github.com:RahmanYazid/hyprland-keyboard-macro.git

cd hyprland-keyboard-macro
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # bash/zsh
# or for fish shell:
source venv/bin/activate.fish

pip install -r requirements.txt
```

### 3. Add your user to the `input` group

The program needs read access to the keyboard device (`/dev/input/eventX`) and write access to `/dev/uinput` to simulate key presses. Both are typically owned by the `input` group.

```bash
sudo usermod -aG input $USER
```

> **Important:** after running this command, you **must log out and log back in** (or restart your PC). Group changes do not take effect in your currently running terminal session.

After logging back in, verify the group is active:

```bash
groups
```

Make sure `input` appears in the output.

### 4. Run the program

```bash
cd <your-repo-folder>
source venv/bin/activate        # or activate.fish for fish shell
python macro.py
```

If successful, the program will list the detected keyboards and be ready to use.

## Usage

1. Run `macro.py` — keep the terminal running in the background
2. Focus your cursor on the target application/text field
3. Press **Insert** to activate the macro (the terminal will print `ON (AKTIF)`)
4. Press **Insert** again to deactivate it (`OFF (MATI)`)
5. Press **Ctrl+C** in the terminal to fully exit the program

## Configuration

All settings are at the top of `macro.py`:

```python
KEY_TO_PRESS = ecodes.KEY_D       # Key to auto-type
TOGGLE_KEY = ecodes.KEY_INSERT    # Key used to toggle ON/OFF
DELAY = 0.5                       # Delay between key presses (in seconds)
```

| Setting        | Description                                                                                                                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `KEY_TO_PRESS` | The key that gets pressed repeatedly. Use `ecodes.KEY_<NAME>` constants, e.g. `ecodes.KEY_E`, `ecodes.KEY_SPACE`, `ecodes.KEY_ENTER`. The full list is available in the `evdev.ecodes` module. |
| `TOGGLE_KEY`   | The physical key used to enable/disable the macro. Can be changed to any rarely-used key, e.g. `ecodes.KEY_HOME`, `ecodes.KEY_END`, `ecodes.KEY_SCROLLLOCK`.                                   |
| `DELAY`        | Delay between key presses, in seconds. Lower values type faster (e.g. `0.1` = 10x/sec, `0.5` = 2x/sec).                                                                                        |

After changing the configuration, save the file and re-run `python macro.py`.

## Troubleshooting

**`ModuleNotFoundError: No module named 'evdev'`**
Make sure the virtual environment is activated (`source venv/bin/activate`) before running `pip install -r requirements.txt` and `python macro.py`.

**`Permission denied` when opening the device**
Make sure your user is in the `input` group (`groups`) and that you've logged out/back in after running `usermod -aG input $USER`.

**The program runs but the Insert toggle isn't detected**
Check whether `macro.py` successfully detected a physical keyboard in the list shown at startup. If the list is empty, `evdev` likely isn't recognizing your device as a keyboard — please open an Issue.

**Want a shortcut command without `cd` and `activate` every time**
Add an alias to your shell config, e.g. for fish (`~/.config/fish/config.fish`):

```fish
alias macro="~/path/to/repo/venv/bin/python ~/path/to/repo/macro.py"
```

## Disclaimer

This script simulates real keyboard input at the system level. Use it responsibly — some applications/games prohibit the use of macros/auto-key tools and may apply penalties according to their own policies.
