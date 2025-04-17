# File Organizer

A modern Python GUI tool to organize your images and documents into folders by month or year.  
Supports common file types including iPhone-specific formats, videos, audio, and archives.

## Features

- Organize files by **month** or **year** based on last modified date
- Supports images, documents, iPhone formats, videos, audio, and archives
- Simple and modern GUI (Tkinter + ttk)
- Safe: Only moves supported files, leaves others untouched

## Usage

1. Install Python 3.x.
2. Run the app:
   ```sh
   python file_organizer.py
   ```
3. Select the folder you want to organize.
4. Choose to organize by month or year.
5. Click **Organize**.

## Supported File Types

- **Images:**  
  `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.heic`, `.heif`, `.livephoto`, `.aae`
- **Videos:**  
  `.mov`, `.mp4`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`
- **Audio:**  
  `.mp3`, `.wav`, `.aac`, `.ogg`, `.opus`, `.wma`, `.m4a`
- **Documents:**  
  `.pdf`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.txt`
- **Archives:**  
  `.zip`, `.rar`

## License

MIT License
