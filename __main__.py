from file_folder_handler import folder, file
from radiate_dropper import radiate_dropper
from pathlib import Path
import shutil
import sys

def main():
    # Clean-up main working directory
    radiate_parent_path = Path('RadiateBuild')
    if radiate_parent_path.exists():
        shutil.rmtree(radiate_parent_path) # will remove path and children

    # Create clean directory
    game_name = sys.argv[1]
    radiate_child_folder_paths = Path(f"{radiate_parent_path}/{game_name}/Game")
    folder.create(radiate_child_folder_paths)

    # Copy the entire contens of ".\Staging\<yourgame>\bin" to "radiate_parent_path}/{game_name}/Game" above
    game_platform = sys.argv[2]
    game_path = Path(f"Staging/{game_name}/bin")
    folder.copy_from_to(game_path, radiate_child_folder_paths)

    # Create a Subdirectory in ".\<RadiateBuilds>\<YourGame>" called "Host"
    radiate_host_directory = Path(f"{radiate_parent_path}/{game_name}/Host")
    folder.create(radiate_host_directory)

    # Copy the entire contents of ".\<YourGDK>\Runtime\Binaries\Tools\GDKRuntimeHost\x64\Release" to ".\<RadiateBuilds>\<YourGame>\Host".
    gdk_path = Path(f"MonacoGames/GDK/Runtime/Binaries/Tools/GDKRuntimeHost/{game_platform}/Release")
    folder.copy_from_to(gdk_path, radiate_host_directory)

    # Grab the HostCommandLineArgs.txt or similar from the MonacoGames > Games > GameName. Modify the file to follow the correct standard.
    host_command_file_path = Path(f"MonacoGames/Games/{game_name}/HostCommandLineArgs.txt")
    game_directory = Path(f"{radiate_parent_path}/{game_name}")
    docs_directory = Path("Docs")
    if file.exists(host_command_file_path):
        # Move the host_command_file_path file & docs_directory (the doc directory has the run.bat) folder content to game_directory
        folder.copy_from_to(docs_directory, game_directory)
        file.copy_from_to(host_command_file_path, str(game_directory) + "/HostCommandLineArgs.txt") # Added the /HostCommandLineArgs.txt because it needs a full file path
    
    # Rename the game folder for the drop
    full_drop_game_name = game_name + "_" + sys.argv[3]
    game_directory = Path(f"RadiateBuild/{game_name}")
    renamed_to = Path(f"RadiateBuild/{full_drop_game_name}")
    folder.rename(game_directory, renamed_to)

    # Run the Radiate "Full drop as <YourGame>" or "Full drop to <YourGame>" on ".\<RadiateBuilds>\<YourGame>"
    radiate_comment_message = sys.argv[4]
    radiate_dropper.full_drop_as_game_console(game_name=full_drop_game_name, message=radiate_comment_message)

if __name__ == "__main__":
    main()
