from sys import argv

from .video import AsciiVideo


if __name__ == "__main__":
    path_to_file: str = argv[1]
    app: AsciiVideo = AsciiVideo(path_to_file)
    app.run()
