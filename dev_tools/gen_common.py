from config_generator import Builder, GenDict, GenStr, GenCustom, build_python, build_toml
from pathlib import Path


def make_builder() -> Builder:
    trigger_mode = GenCustom(
        parse_command="TriggerMode.safe_from_str($value)", config_value=GenStr("one_shot"), code_type="TriggerMode")
    # Initialize builder with TOML formatting settings matching the example
    builder = Builder(
        code_indent="    ",
        config_indent="  ",
        config_new_line="\n",
        code_new_line="\n",
        config_comment_sep=" ",
        import_statements=["from trigger_modes import TriggerMode"]
    )
    builder.comment(
        " NOTE: through this file I will refer to macro mode as the mode you are in that intercepts your keystrokes to execute macros")
    builder.comment(
        " whereas normal mode is the default mode where your key strokes are processed normally as if the program weren't running")
    builder.new_line()
    builder.add_section("general")
    builder.comment(
        " NOTE: the trigger key should be a key that you don't use for other purposes")
    builder.comment(
        " as it will be intercepted by the program and other programs won't see you press it")
    builder.add_str("trigger_key", "menu")

    builder.comment(
        " trigger_modes lets you set how you want to activate/deactivate macro mode ")
    builder.comment(
        " toggle will make it so that each time you press the trigger_key it will toggle between macro mode and normal mode")
    builder.comment(
        " hold makes it so that you are only in macro mode while you hold down the trigger key")

    builder.comment(
        " one_shot, the default, maintains the same behavior as hold except if you press the trigger_key without triggering any macros between you pressing it and releasing it, it will treat the next key strokes as a trigger, until you trigger a macro or hit the trigger_key again.")
    builder.add_field("trigger_mode", trigger_mode)
    builder.new_line()
    section = "macros"
    builder.add_custom_section(
        section, f'$map.get("{section}") or {{}}', GenDict)
    builder.comment(
        " macros for their value should follow the form <command> or <command> <params>")
    builder.new_line()
    builder.comment(
        " run_user <script> runs a script sourced from the <config_dir>/scripts directory")
    builder.comment(
        " the <script> must be a name that matches a executable in that directory if you want it to run")

    builder.new_line()

    builder.comment(
        " run_root <script> runs scripts sourced from /etc/macro_misdirect/scripts")
    builder.comment(
        " the script must exist, be executable and usually needs a shebang if it is a shell file")
    builder.comment(
        " I suppose you could also technically put a executable binary in that directory as well")

    builder.new_line()

    builder.comment(
        " write <text> will write whatever the text is")

    builder.new_line()
    builder.comment(
        " reload puts the user back in normal mode and reloads the config.")
    builder.new_line()
    builder.comment(
        " terminate, terminates the program")
    builder.new_line()
    builder.comment("examples:")

    builder.add_str("cn", "run_user cool_not")
    builder.add_str("dw", "run_user double_who")
    builder.add_str("dww", "run_user who")
    builder.add_str("sw", "run_root who")
    builder.add_str("ng", "write nothing ")
    builder.add_str("rl", "reload")
    builder.add_str("tm", "terminate")
    return builder


def example_config_path() -> str:
    return str(_root_dir()/"example_config.toml")


def python_path() -> str:
    return str(_root_dir()/"config.py")


def make_python(builder: Builder) -> str:
    return build_python(builder)


def make_toml(builder: Builder) -> str:
    return build_toml(builder)


def _root_dir():
    return Path(__file__).resolve().parent.parent
