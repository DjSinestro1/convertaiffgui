import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class AudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Converter")
        self.target_frames = []
        
        # Creator Label
        creator_label = tk.Label(root, text="Chris Sinestro made this badboy, aww yeah", font=("Helvetica", 12))
        creator_label.pack(pady=10)
        
        # Source Directory
        self.frame_source = tk.Frame(root)
        self.frame_source.pack(padx=10, pady=5)
        label_source = tk.Label(self.frame_source, text="Select Source Directory:")
        label_source.grid(row=0, column=0, padx=5, pady=5)
        self.entry_source = tk.Entry(self.frame_source, width=50)
        self.entry_source.grid(row=0, column=1, padx=5, pady=5)
        button_browse = tk.Button(self.frame_source, text="Browse", 
                                command=lambda: self.browse_directory(self.entry_source))
        button_browse.grid(row=0, column=2, padx=5, pady=5)
        
        # Container for target directories
        self.targets_container = tk.Frame(root)
        self.targets_container.pack(padx=10, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)
        
        add_button = tk.Button(buttons_frame, text="Add Target Directory", 
                             command=self.add_target_directory)
        add_button.pack(side=tk.LEFT, padx=5)
        
        remove_button = tk.Button(buttons_frame, text="Remove Last Target", 
                                command=self.remove_target_directory)
        remove_button.pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.button_convert = tk.Button(root, text="Convert Files", 
                                      command=self.start_conversion)
        self.button_convert.pack(pady=20)
        
        # Add first target directory by default
        self.add_target_directory()

    def add_target_directory(self):
        frame = tk.Frame(self.targets_container)
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        label = tk.Label(frame, text=f"Target Directory {len(self.target_frames) + 1}:")
        label.grid(row=0, column=0, padx=5, pady=5)
        
        entry = tk.Entry(frame, width=50)
        entry.grid(row=0, column=1, padx=5, pady=5)
        
        browse_button = tk.Button(frame, text="Browse", 
                                command=lambda e=entry: self.browse_directory(e))
        browse_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.target_frames.append((frame, entry))

    def remove_target_directory(self):
        if len(self.target_frames) > 1:
            frame, _ = self.target_frames.pop()
            frame.destroy()

    def browse_directory(self, entry_widget):
        directory = filedialog.askdirectory()
        if directory:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, directory)

    def start_conversion(self):
        source_directory = self.entry_source.get()
        target_directories = [entry.get() for _, entry in self.target_frames]
        
        if not os.path.isdir(source_directory):
            messagebox.showerror("Error", "Please select a valid source directory.")
            return
            
        for target_dir in target_directories:
            if not os.path.isdir(target_dir):
                messagebox.showerror("Error", f"Invalid target directory: {target_dir}")
                return
                
        self.convert_to_aiff(source_directory, target_directories)

    def convert_to_aiff(self, source_directory, target_directories):
        files_converted = 0
        files_deleted = 0

        for dirpath, dirnames, filenames in os.walk(source_directory):
            for filename in filenames:
                if filename.endswith(('.wav', '.flac', '.mp4')):
                    input_file = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(dirpath, source_directory)
                    output_dir = os.path.join(source_directory, relative_path)
                    
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    output_file = os.path.join(output_dir, 
                                             os.path.splitext(filename)[0] + '.aiff')
                    
                    if filename.endswith('.mp4'):
                        command = ['ffmpeg', '-y', '-i', input_file, '-vn', 
                                 '-c:a', 'pcm_s16be', output_file]
                    else:
                        command = ['ffmpeg', '-y', '-i', input_file, 
                                 '-c:a', 'pcm_s16be', output_file]

                    try:
                        subprocess.run(command, check=True)
                        print(f'Converted {input_file} to {output_file}')
                        
                        if os.path.exists(output_file):
                            files_converted += 1
                            
                            for target_directory in target_directories:
                                target_file = os.path.join(target_directory, 
                                                         os.path.basename(output_file))
                                target_file_dir = os.path.dirname(target_file)
                                
                                if not os.path.exists(target_file_dir):
                                    os.makedirs(target_file_dir)
                                
                                try:
                                    if os.path.normpath(output_file) != os.path.normpath(target_file):
                                        shutil.copy2(output_file, target_file)
                                        print(f'Copied {output_file} to {target_file}')
                                except shutil.SameFileError:
                                    print(f'Skipping copy - Source and destination are the same: {target_file}')
                            
                            os.remove(input_file)
                            files_deleted += 1
                    except subprocess.CalledProcessError as e:
                        print(f"Error converting {input_file}: {e}")

        if files_converted == files_deleted:
            messagebox.showinfo("Success", 
                              f"Converted and deleted {files_converted} files.")
        else:
            messagebox.showwarning("Warning", 
                                 f"Converted: {files_converted}, Deleted: {files_deleted}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverter(root)
    root.mainloop()
