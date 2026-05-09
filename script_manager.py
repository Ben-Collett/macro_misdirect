from config_manager import ConfigManager
from constants import SCRIPT_DIR_NAME, ROOT_SCRIPT_PATH
from pathlib import Path


def get_user_script_path(name, config_manager: ConfigManager) -> Path:
    return config_manager.find_config_dir_path()/SCRIPT_DIR_NAME/name


def get_root_script_path(name) -> Path:
    return Path(ROOT_SCRIPT_PATH)/name
