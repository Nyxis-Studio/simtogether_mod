import os
from pathlib import Path

# ####################################################
# Settings you can change
# ####################################################

# Your Name
creator_name = 'CREATOR_NAME'

# Sims 4 mod folder location
mods_folder = os.path.expanduser(
    os.path.join('~', 'Documents', 'Electronic Arts', 'The Sims 4', 'Mods')
)

# Location of folder to contain your projects
projects_folder = os.path.expanduser(
    os.path.join('~', 'Documents', 'Sims 4 Projects')
)

# Location of the game folder
# Game folder for steam users
game_folder = os.path.join('C:', os.sep, 'Program Files (x86)', 'Steam', 'steamapps', 'common', 'The Sims 4')

# Game folder for EA launcher users
#game_folder = os.path.join('C:', os.sep, 'Program Files', 'EA Games', 'The Sims 4')

# ONLY FOR USERS OF PYCHARM PRO: Location of PyCharm Professional for debug setup
# You do not need to use PyCharm at all or the professional version, ignore this setting if you are not
pycharm_pro_folder = os.path.join('C:', os.sep, 'Program Files', 'JetBrains', 'PyCharm Community Edition 2024.3.3')

# ####################################################
# Settings that you can but generally won't change
# ####################################################

# Folder within this project that contains your python/script files
src_subpath = "src"

# Folder within this project that your mods will be built to
build_subpath = "build"

# To hold asset files like xml tuning files and packages
assets_subpath = "assets"

# To hold EA decompiled files to make your mod
ea_files_subpath = "ea"


# Subpath inside the projects folder to place decompiled python files
projects_python_subpath = "__util" + os.sep + "Python"
projects_tuning_subpath = "__util" + os.sep + "Tuning"

# The name of this project, by default it's setup to use the folder name containing the project
project_name = Path(__file__).parent.stem

# Dev Mode
devmode_cmd_mod_src = "Utility/devmode_cmd.py"
devmode_cmd_mod_name = "devmode-cmd"

# The name of the mod which will start the Pycharm debugging when entered into the game
# ONLY FOR PYCHARM PRO USERS: If you're not using PyCharm Pro don't worry about this setting
debug_cmd_mod_name = "pycharm-debug-cmd"
debug_cmd_mod_src = "Utility/debug_cmd.py"
debug_capability_name = "pycharm-debug-capability"
debug_mod_subfolder = "PyCharmPro_Debug"

# ####################################################
# Settings that don't make any sense for you to change
# ####################################################

# The project folder path itself
root_path = str(Path(__file__).parent)

# These paths are calculated from the above information
src_path = os.path.join(root_path, src_subpath)
build_path = os.path.join(root_path, build_subpath)
assets_path = os.path.join(root_path, assets_subpath)
ea_files_path = os.path.join(root_path, ea_files_subpath)
devmode_cmd_mod_src_path = os.path.join(Path(__file__).parent, devmode_cmd_mod_src)
projects_python_path = os.path.join(projects_folder, projects_python_subpath)
projects_tuning_path = os.path.join(projects_folder, projects_tuning_subpath)
debug_cmd_mod_src_path = os.path.join(Path(__file__).parent, debug_cmd_mod_src)

# Sims 4 Data and Game Folders
gameplay_folder_data = os.path.join(game_folder, 'Data', 'Simulation', 'Gameplay')
gameplay_folder_game = os.path.join(game_folder, 'Game', 'Bin', 'Python')
debug_eggs_path = os.path.join(pycharm_pro_folder, "debug-eggs", "pydevd-pycharm.egg")
