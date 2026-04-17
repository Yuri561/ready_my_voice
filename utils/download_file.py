from tkinter import filedialog

def download_file(file_path, filedialog_module=filedialog, text_widget=None):
    if not file_path:
        return

    save_path = filedialog_module.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")]
    )

    if save_path:
        try:
            with open(file_path, "rb") as src, open(save_path, "wb") as dst:
                dst.write(src.read())
        except Exception as e:
            print(f"Download failed: {e}")
            if text_widget:
                text_widget.insert("end", f"Download failed: {e}\n")
                text_widget.see("end")
                
