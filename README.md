# Macro Misdirect
Macro Misdirect is a program to allow you to define nearly infinitely many macros that someone watching
your screen would not be able to see are being triggered.

Useful for content creators or people who are running out of ways to set keybindings.

This project is meant to feel somewhate similar to using keymaps in vim.

## Platforms
Currently, **Linux only** (requires root privileges or being part of the input and tty groups).

## Installation
You can just clone the repo and run `python main.py` though you will likely need root privileges.

If you use [dumb_installer](https://github.com/Ben-Collett/dumb_installer) then run `sudo din Ben-Collett/macro_misdirect`.
The default installed command will be `mcmd`.

## External Dependencies
- Python
- runuser command, should be installed on most Linux systems
- tomlkit - optional if not installed then tomllib is used to parse the config which is in most Python versions by default.

## How it works
Macro Misdirect has two modes: normal and macro mode.


Macro Misdirect grabs exclusive access to your keyboards and uses a virtual keyboard to propagate key events when in normal mode.
With the exception of the trigger key which when pressed will **NOT** be sent to the desktop environment and instead will activate macro mode depending on the trigger_mode settings.

When in macro mode no key strokes will reach the desktop environment (except for through write macros). And instead they will be used to run macros.

If the keys you have typed in macro mode match a macro and only one possible macro then that macro will be triggered automatically. Otherwise, you need to press space to trigger the macro. If you mess up typing a macro, hit space to essentially clear the current macro you're typing and move on to the next one (or you could exit macro mode but that is often less ergonomic).

## Warning
Macro Misdirect relies on being able to discern its own key events to trigger write macros, so if you want to use write macros avoid having the virtual keyboard created by the program grabbed by another keyboard program.

Also for security reasons if you are running this program as root then you should put it somewhere where only the root user can access it. This is handled automatically by dumb_installer if you use that.


## Configuration
You should define a config.toml in `~/.config/macro_misdirect`.

You should define any scripts you want to run with user privileges in `~/.config/macro_misdirect/scripts`.

You should define any scripts you want to run with root privileges in `/etc/macro_misdirect/scripts/`.


See the [example_config.toml](example_config.toml) which is an example config with all options available.


## License

This project is dual-licensed:
- **Full license**: see [LICENSE](LICENSE)
- **Keyboard module**: MIT License (see [licenses/KEYBOARD_LICENSE](licenses/KEYBOARD_LICENSE))
- **The rest of the project**: BSD Zero Clause License (see [licenses/MAIN_LICENSE](licenses/MAIN_LICENSE))
