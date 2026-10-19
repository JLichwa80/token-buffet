"""Native OS folder chooser (tkinter). `python -m tokenbuffet.folder_picker` prints the chosen path."""


def pick_folder():
    """Return the chosen folder path, or '' when cancelled."""
    from tkinter import Tk, filedialog
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askdirectory(title="Choose the app folder", mustexist=False)
    finally:
        root.destroy()


if __name__ == "__main__":
    print(pick_folder())
