import os
import sys
from datetime import datetime
from mutagen.mp3 import MP3
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent # get parent directory of "utils" directory
static_podcasts_dir = str(Path(parent_dir)) + "/" + "static_podcasts"
print(sys.argv[1:])
def main():
    print("")
    print("---")
    print("")
    if len(sys.argv) > 1:
        args = "".join(sys.argv[1:])
        audio_file = static_podcasts_dir + "/" + args + ".mp3"
        if Path(audio_file).exists():
            print(f"Podcast source audio file found by ID: {args}")
            print("")
            filesize = os.path.getsize(audio_file)
            audio = MP3(audio_file)
            seconds = int(audio.info.length)
            print(f"Podcast file size in bytes: {filesize}")
            print("")
            print(f"Podcast audio length in seconds: {seconds}")
            print("")
            minutes, sec = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            hh_mm_ss = f"{hours:02d}:{minutes:02d}:{sec:02d}"
            print(f"Podcast audio length in HH:MM:SS: {hh_mm_ss}")
            print("")
        else:
            print("Podcast source audio file NOT FOUND")
    else:
        print("Only 1 argument is required: the 8 character podcast file ID")
    print("")
    print("---")
    print("")


if __name__ == "__main__":
    main()

