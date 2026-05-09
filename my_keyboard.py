from keyboard import init, hook, wait, propagate,write, KeyboardEvent
_KEYBOARD_NAME = "misdirected_marco_keyboard"
class MyKeyboard:
    def __init__(self):
        init(auto_grab=True, device_name=_KEYBOARD_NAME)

    def write(self, text:str):
        write(text)

    def propagate(self,event):
        propagate(event)

    def hook(self,callback):
        def filtered_callback(event:KeyboardEvent):
            if event.device_name != _KEYBOARD_NAME:
                callback(event)
        hook(filtered_callback)


    def wait(self):
        wait()




