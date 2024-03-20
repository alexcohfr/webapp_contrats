import glob
import os.path
import os
import shutil



def remove_cache():
    """Remove all files in the "cache" folder
    """
    folder_path = './public/cache/'
    file_type = '*.docx'
    try:
        files = glob.glob(os.path.join(folder_path, file_type))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
        return True
    except:
        return False


def get_latest_contrat():
    folder_path = './public/cache/'
    file_type = '*.docx'
    files = glob.glob(os.path.join(folder_path, file_type))

    if files:  # check if the list of files is not empty
        max_file = max(files, key=os.path.getctime)
        return os.path.basename(max_file)
    else:
        return None

def move_file_to_archive():
    """Move the latest contract in the "cache" folder to the "contrats_generes" folder
    """
    last_file = get_latest_contrat()
    if last_file is not None:
        print("ici")
        shutil.move(f"./public/cache/{last_file}", f"./public/contrats_generes/")
        print("là")
        return True
    else:
        return False

if __name__ == "__main__":
    move_file_to_archive()