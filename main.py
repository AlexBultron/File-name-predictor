import os
import pytesseract
import fitz  # PyMuPDF
import docx
from tkinter import filedialog, Tk, messagebox, Button, Label, Entry

from PIL import Image
from datetime import datetime

# Optional: Set Tesseract path manually (if needed)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""

    try:
        if ext == ".pdf":
            doc = fitz.open(filepath)
            for page in doc:
                text += page.get_text()
        elif ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        elif ext == ".docx":
            d = docx.Document(filepath)
            text = "\n".join([p.text for p in d.paragraphs])
        elif ext in [".jpg", ".jpeg", ".png"]:
            text = pytesseract.image_to_string(Image.open(filepath))
        else:
            messagebox.showerror("Unsupported", "Only PDF, TXT, DOCX, JPG, PNG supported.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    return text.strip()

def predict_name(text):
    text = text.lower()

    if "invoice" in text:
        return f"Invoice_{datetime.now().strftime('%B%Y')}.pdf"
    elif "resume" in text or "curriculum vitae" in text:
        name = "John_Doe"
        return f"Resume_{name}.pdf"
    elif "meeting" in text or "notes" in text:
        return f"Meeting_Notes_{datetime.now().strftime('%B%d')}.txt"
    elif "report" in text:
        return f"Report_{datetime.now().strftime('%Y%m%d')}.pdf"
    else:
        return f"Document_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)
        content = extract_text(file_path)
        suggestion = predict_name(content)
        entry_name.delete(0, 'end')
        entry_name.insert(0, suggestion)

def rename_file():
    old_path = file_label.cget("text")
    new_name = entry_name.get()

    if not old_path or not new_name:
        messagebox.showerror("Missing Info", "Please choose a file and enter a name.")
        return

    folder = os.path.dirname(old_path)
    new_path = os.path.join(folder, new_name)

    try:
        os.rename(old_path, new_path)
        messagebox.showinfo("Success", f"File renamed to:\n{new_name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = Tk()
root.title("🧠 Smart File Name Predictor")
root.geometry("600x200")

Label(root, text="Step 1: Choose a file").pack()
Button(root, text="Browse File", command=browse_file).pack(pady=5)
file_label = Label(root, text="", wraplength=500)
file_label.pack()

Label(root, text="Step 2: Suggested filename").pack()
entry_name = Entry(root, width=60)
entry_name.pack()

Button(root, text="Rename File", command=rename_file).pack(pady=10)

root.mainloop()
