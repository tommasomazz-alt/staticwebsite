import os
import shutil
from copystatic import static_to_public

def main() -> None:

    if "public" in os.listdir("./"):
        shutil.rmtree("./public")

    os.mkdir("./public")
    
    static_to_public("static","public")

main()