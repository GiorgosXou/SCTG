import platform
OPERATING_SYSTEM = platform.system()

 
if OPERATING_SYSTEM == 'Windows': 
    def __copy_image(path): pass

elif OPERATING_SYSTEM == 'Darwin': 
    def __copy_image(path): pass

else: # https://stackoverflow.com/a/67364677/11465149
    import os
    def __copy_image(path):
        os.system(f"xclip -selection clipboard -t image/png -i '{path}'")

def copy_image(path):
     __copy_image(path)
