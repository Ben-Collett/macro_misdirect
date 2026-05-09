from enum import Enum


class TriggerMode(Enum):
    ONE_SHOT = "one_shot"
    HOLD = "hold"
    TOGGLE = "toggle"

    @staticmethod
    def safe_from_str(value: str):
        toggle_modes = [member.value for member in TriggerMode]
        if value in toggle_modes:
            return TriggerMode(value)
        print(f"{value} is not a valid toggle mode: {toggle_modes}")
        print(f"defaulting to {TriggerMode.ONE_SHOT.value}")
        return TriggerMode.ONE_SHOT
