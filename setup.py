from cx_Freeze import setup, Executable

base = None    

executables = [Executable("interface.py", base=base)]

packages = ["stock_pull_A_0", "texteditor", "matplotlib", "os", "datetime", "time",
            "urllib", "csv", "tkinter", "threading", "graphics_A_0", "operator",
            "numpy", "sys"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "FAT: Financial Analysis Tools",
    options = options,
    version = "1.0.0",
    description = '<any description>',
    executables = executables
)
