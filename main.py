from config_manager import ConfigManager
from my_keyboard import MyKeyboard
from config import Config
from keyboard import KeyboardEvent, KEY_DOWN
from script_manager import get_root_script_path, get_user_script_path
from shell_runner import run_as_root, run_as_user
import sys
from trigger_modes import TriggerMode
from utils import to_utf
from constants import APP_NAME
import threading
from dataclasses import dataclass
from load_config_map import parse
from typing import Optional


@dataclass
class GlobalData:
    config: Config
    keyboard: MyKeyboard
    config_manager: ConfigManager
    terminate_event: threading.Event
    hook_handler: Optional['HookHandler'] = None


def process_str(command: str, global_data: GlobalData):
    keyboard = global_data.keyboard
    terminate_event = global_data.terminate_event
    config_manager = global_data.config_manager
    WRITE_COMMAND = "write "
    TERMINATE = "terminate"
    RELOAD = "reload"
    RUN_USER = "run_user "
    RUN_ROOT = "run_root "

    if command.startswith(TERMINATE):
        terminate_event.set()
    elif command.startswith(RELOAD):
        if global_data.hook_handler:
            global_data.hook_handler.reload()
        else:
            print("BUG: there no hook handler, somehow.")
    elif command.startswith(WRITE_COMMAND):
        keyboard.write(command.removeprefix(WRITE_COMMAND))
    elif command.startswith(RUN_USER):
        run_as_user(get_user_script_path(
            command.removeprefix(RUN_USER), config_manager))
    elif command.startswith(RUN_ROOT):
        run_as_root(get_root_script_path(command.removeprefix(RUN_ROOT)))


def process(to_process: str | list[str], global_data: GlobalData):
    if isinstance(to_process, str):
        to_process = [to_process]

    for command in to_process:
        process_str(command, global_data)


def is_space(event):
    return event.name == "space"


def _should_trigger(event: KeyboardEvent, current_trigger: str, config: Config) -> bool:
    is_pressed = event.event_type == KEY_DOWN
    if not is_pressed:
        return False
    if is_space(event):
        return True
    contains_trigger = False
    for command in config.macros:
        if command.startswith(current_trigger):
            contains_trigger = True
            if command != current_trigger:
                return False

    return contains_trigger


class HookHandler:
    def __init__(self, global_data: GlobalData):
        self.global_data = global_data
        self.keyboard = global_data.keyboard
        self.is_triggered = False
        self.already_triggered = False
        self.trigger_down = False
        self.triggered_in_one_shot_cycle = False
        self.current_trigger = ""

    def reload(self):
        data = _load_toml(self.global_data.config_manager)
        self.global_data.config = Config(data)
        self.is_triggered = False
        self.trigger_down = False
        self.already_triggered = False
        self.triggered_in_one_shot_cycle = False
        self.current_trigger = ""

    def __call__(self, event: KeyboardEvent):
        config = self.global_data.config
        is_pressed = event.event_type == KEY_DOWN
        is_trigger_key = event.name == config.general.trigger_key
        mode = config.general.trigger_mode

        if is_trigger_key and is_pressed:
            self.already_triggered = self.is_triggered
            self.trigger_down = True
            if mode == TriggerMode.TOGGLE:
                self.is_triggered = not self.is_triggered
            elif mode == TriggerMode.HOLD or mode == TriggerMode.ONE_SHOT:
                self.is_triggered = True
        elif is_trigger_key:
            self.trigger_down = False
            one_shot = mode == TriggerMode.ONE_SHOT
            if mode == TriggerMode.HOLD or (one_shot and (self.triggered_in_one_shot_cycle or self.already_triggered)):
                self.triggered_in_one_shot_cycle = False
                self.already_triggered = False
                self.current_trigger = ""
                self.is_triggered = False

        if self.is_triggered:
            if is_pressed and not is_space(event):
                utf = to_utf(event)
                if utf:
                    self.current_trigger += utf

            should_trigger = _should_trigger(
                event, self.current_trigger, config)
            if should_trigger:
                if self.current_trigger in config.macros:
                    process(
                        config.macros[self.current_trigger], self.global_data)
                    if mode == TriggerMode.ONE_SHOT:
                        self.triggered_in_one_shot_cycle = True
                    if mode == TriggerMode.ONE_SHOT and not self.trigger_down:
                        self.triggered_in_one_shot_cycle = False
                        self.is_triggered = False
                self.current_trigger = ""
        else:
            self.keyboard.propagate(event)


def _load_toml(manager: ConfigManager) -> dict:
    path = manager.find_config_file("config.toml")
    out = {}
    if path.exists():
        out = parse(manager.find_config_file("config.toml")) or out

    return out


def main():
    terminate_event = threading.Event()
    keyboard = MyKeyboard()
    config_manager = ConfigManager(APP_NAME)
    data = _load_toml(config_manager)

    global_data = GlobalData(
        config_manager=config_manager,
        config=Config(data), keyboard=keyboard, terminate_event=terminate_event)
    hook_handler = HookHandler(global_data)
    global_data.hook_handler = hook_handler
    keyboard.hook(hook_handler)

    try:
        terminate_event.wait()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
