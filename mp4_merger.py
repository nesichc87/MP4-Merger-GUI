import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips

class MP4MergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 Merger")
        self.root.geometry("500x400")

        self.file_list = []

        # UI-Elemente
        self.label = tk.Label(root, text="Wähle MP4-Dateien aus:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Dateien auswählen", command=self.select_files)
        self.select_button.pack(pady=5)

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.up_button = tk.Button(root, text="⬆ Nach oben", command=self.move_up)
        self.up_button.pack(pady=5)

        self.down_button = tk.Button(root, text="⬇ Nach unten", command=self.move_down)
        self.down_button.pack(pady=5)

        self.output_label = tk.Label(root, text="Speicherort wählen:")
        self.output_label.pack(pady=10)

        self.save_button = tk.Button(root, text="Speichern unter...", command=self.save_file)
        self.save_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Videos zusammenfügen", command=self.merge_videos)
        self.merge_button.pack(pady=10)

        self.output_path = ""

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("MP4 Dateien", "*.mp4")])
        if files:
            self.file_list = list(files)
            self.update_listbox()
            messagebox.showinfo("Erfolg", f"{len(files)} Dateien ausgewählt!")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.file_list:
            self.listbox.insert(tk.END, file)

    def move_up(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0]
            self.file_list[index], self.file_list[index - 1] = self.file_list[index - 1], self.file_list[index]
            self.update_listbox()
            self.listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < len(self.file_list) - 1:
            index = selected_index[0]
            self.file_list[index], self.file_list[index + 1] = self.file_list[index + 1], self.file_list[index]
            self.update_listbox()
            self.listbox.select_set(index + 1)

    def save_file(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Dateien", "*.mp4")])
        if self.output_path:
            messagebox.showinfo("Speicherort", f"Speichert unter: {self.output_path}")

    def merge_videos(self):
        if not self.file_list or not self.output_path:
            messagebox.showerror("Fehler", "Bitte wähle Dateien und einen Speicherort aus!")
            return

        clips = [VideoFileClip(file) for file in self.file_list]
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(self.output_path, codec="libx264", fps=30)

        messagebox.showinfo("Fertig", "Das Video wurde erfolgreich gespeichert!")

# App starten
root = tk.Tk()
app = MP4MergerApp(root)
root.mainloop()
