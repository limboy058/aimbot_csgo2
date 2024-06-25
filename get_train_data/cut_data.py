#将数据划分为train,val,test

import os
import shutil
import random


def copy_files_to_dirs(src_dir, dest_dirs):
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    
    for file in files:
        src_file_path = os.path.join(src_dir, file)

        t=random.random()
        if t<=0.1:
            chosen_dir=dest_dirs[0]
        elif t<=0.9:
            chosen_dir=dest_dirs[1]
        else:
            chosen_dir=dest_dirs[2]
        

        shutil.copy(src_file_path, chosen_dir)
        print(f"Copied {file} to {chosen_dir}")

if __name__ == "__main__":

    source_directory = 'C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\pic'
    

    destination_directories = [
        'C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\csgo2\\test\\images',
        'C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\csgo2\\train\\images',
        'C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\csgo2\\valid\\images'
    ]
    

    copy_files_to_dirs(source_directory, destination_directories)
