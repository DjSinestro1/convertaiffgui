import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_to_aiff(source_directory, target_directories):
    # Counters for tracking conversions and deletions
    files_converted = 0
    files_deleted = 0
    
    # Walk through the directory and subdirectories
    for dirpath, dirnames, filenames in os.walk(source_directory):
        for filename in filenames:
            if filename.endswith('.wav') or filename.endswith('.flac'):
                input_file = os.path.join(dirpath, filename)
                # Maintain the original directory structure for AIFF files
                relative_path = os.path.relpath(dirpath, source_directory)
                output_dir = os.path.join(source_directory, relative_path)  
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.aiff')
                
                # FFmpeg command to convert audio file to AIFF
                command = ['ffmpeg', '-y', '-i', input_file, '-c:a', 'pcm_s16be', output_file]
                
                # Execute the command
                try:
                    subprocess.run(command, check=True)
                    print(f'Converted {input_file} to {output_file}')
                    
                    # Check if the output file was created successfully
                    if os.path.exists(output_file):
                        files_converted += 1
                        # Copy the converted file to each target directory
                        for target_directory in target_directories:
                            target_file = os.path.join(target_directory, relative_path, os.path.basename(output_file))
                            target_file_dir = os.path.dirname(target_file)
                            if not os.path.exists(target_file_dir):
                                os.makedirs(target_file_dir)
                            shutil.copy2(output_file, target_file)
                            print(f'Copied {output_file} to {target_file}')
                        
                        # Delete the original file after conversion
                        os.remove(input_file)
                        files_deleted += 1
                        print(f'Deleted original file: {input_file}')
                    else:
                        print(f"Failed to create AIFF file for {input_file}")
                        
                except subprocess.CalledProcessError as e:
                    print(f"Error converting {input_file}: {e}")

    # Final check to ensure equal number of conversions and deletions
    if files_converted == files_deleted:
        messagebox.showinfo("Conversion Complete", f"All files converted and deleted successfully: {files_converted} files.")
    else:
        messagebox.showwarning("Conversion Warning", f"Mismatch in conversion and deletion counts: {files_converted} converted, {files_deleted} deleted.")

def browse_directory(entry_widget):
    directory = filedialog.askdirectory()
    if directory:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

def start_conversion():
    source_directory = entry_source_directory.get()
    target_directories = [entry_target_directory_1.get(), entry_target_directory_2.get(), entry_target_directory_3.get()]
    
    if not os.path.isdir(source_directory):
        messagebox.showerror("Error", "Please select a valid source directory.")
        return
    
    for target_directory in target_directories:
        if not os.path.isdir(target_directory):
            messagebox.showerror("Error", f"Please select a valid target directory: {target_directory}.")
            return
    
    convert_to_aiff(source_directory, target_directories)

# Create the main window
root = tk.Tk()
root.title("Audio Converter")

# Creator Label at the top with styled text for "Sinestro"
creator_label = tk.Label(root, text="Chris Sinestro made this badboy, aww yeah", font=("Helvetica", 12))
creator_label.pack(pady=10)

# Source Directory selection
frame_source = tk.Frame(root)
frame_source.pack(padx=10, pady=5)

label_source_directory = tk.Label(frame_source, text="Select Source Directory:")
label_source_directory.grid(row=0, column=0, padx=5, pady=5)

entry_source_directory = tk.Entry(frame_source, width=50)
entry_source_directory.grid(row=0, column=1, padx=5, pady=5)

button_browse_source = tk.Button(frame_source, text="Browse", command=lambda: browse_directory(entry_source_directory))
button_browse_source.grid(row=0, column=2, padx=5, pady=5)

# Target Directory 1 selection
frame_target_1 = tk.Frame(root)
frame_target_1.pack(padx=10, pady=5)

label_target_directory_1 = tk.Label(frame_target_1, text="Select Target Directory 1:")
label_target_directory_1.grid(row=1, column=0, padx=5, pady=5)

entry_target_directory_1 = tk.Entry(frame_target_1, width=50)  # No default path set here
entry_target_directory_1.grid(row=1,column=1,padx=5,pady=5)

button_browse_target_1=tk.Button(frame_target_1,text="Browse",command=lambda:browse_directory(entry_target_directory_1))
button_browse_target_1.grid(row=1,column=2,padx=5,pady=5)

# Target Directory 2 selection
frame_target_2=tk.Frame(root)
frame_target_2.pack(padx=10,pady=5)

label_target_directory_2=tk.Label(frame_target_2,text="Select Target Directory 2:")
label_target_directory_2.grid(row=2,column=0,padx=5,pady=5)

entry_target_directory_2=tk.Entry(frame_target_2,width=50)
entry_target_directory_2.grid(row=2,column=1,padx=5,pady=5)

button_browse_target_2=tk.Button(frame_target_2,text="Browse",command=lambda:browse_directory(entry_target_directory_2))
button_browse_target_2.grid(row=2,column=2,padx=5,pady=5)

# Target Directory 3 selection
frame_target_3=tk.Frame(root)
frame_target_3.pack(padx=10,pady=5)

label_target_directory_3=tk.Label(frame_target_3,text="Select Target Directory 3:")
label_target_directory_3.grid(row=3,column=0,padx=5,pady=5)

entry_target_directory_3=tk.Entry(frame_target_3,width=50)
entry_target_directory_3.grid(row=3,column=1,padx=5,pady=5)

button_browse_target_3=tk.Button(frame_target_3,text="Browse",command=lambda:browse_directory(entry_target_directory_3))
button_browse_target_3.grid(row=3,column=2,padx=5,pady=5)

# Conversion button
button_convert=tk.Button(root,text="Convert Files",command=start_conversion)
button_convert.pack(pady=(20))

# Run the application
root.mainloop()