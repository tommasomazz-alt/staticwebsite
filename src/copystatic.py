import os
import shutil

def static_to_public(src, dst) -> None:
    if not os.path.exists(dst):
        os.mkdir(dst)

    to_copy = os.listdir(src)

    for item in to_copy:
        source_path = os.path.join(src,item)
        destination_path = os.path.join(dst,item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)

        else:
            os.mkdir(destination_path)
            static_to_public(source_path, destination_path)