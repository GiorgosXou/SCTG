
import platform
OPERATING_SYSTEM = platform.system()


if OPERATING_SYSTEM == 'Windows': # https://stackoverflow.com/a/58355052/11465149
    from ctypes import windll, create_unicode_buffer
    def __get_focused_window(): # pacman
        hWnd   = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf    = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)
        return buf.value if buf.value else ''

elif OPERATING_SYSTEM == 'Darwin': 
    from AppKit import NSWorkspace
    def __get_focused_window(): # pacman
        return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()

else: # https://stackoverflow.com/a/72680194/11465149
    from subprocess import run
    def __get_focused_window(): # pacman
        return run(['xdotool', 'getwindowfocus', 'getwindowname'], capture_output=True).stdout.decode('utf-8')


def get_focused_window():
    return __get_focused_window().strip()
