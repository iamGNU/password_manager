import json
import os
import secrets
import string
import sys
from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, StringVar, BooleanVar, messagebox, ttk

import pyperclip

APP_NAME = "PasswordManager"


def resource_dir():
    """Folder holding bundled files like logo.png.

    In a PyInstaller .exe this is the temporary folder the bundle unpacks to.
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def data_dir():
    """Folder where data.json and config.json are kept.

    Running from source: the project folder (as before).
    Running as an .exe: %APPDATA%\\PasswordManager, because the .exe's own
    folder is temporary and may not be writable.
    PASSWORD_MANAGER_DATA_DIR overrides both.
    """
    override = os.environ.get("PASSWORD_MANAGER_DATA_DIR")
    if override:
        folder = Path(override)
    elif getattr(sys, "frozen", False):
        folder = Path(os.environ.get("APPDATA", Path.home())) / APP_NAME
    else:
        folder = Path(__file__).resolve().parent
    folder.mkdir(parents=True, exist_ok=True)
    return folder


DATA_DIR = data_dir()
DATA_FILE = DATA_DIR / "data.json"
CONFIG_FILE = DATA_DIR / "config.json"
LOGO_FILE = resource_dir() / "logo.png"

CLIPBOARD_CLEAR_MS = 30_000
STATUS_CLEAR_MS = 6_000
SYMBOLS = "!#$%&()*+-_=?@^~"
HIDDEN_CHAR = "•"
SHORTCUT_HINT = "Enter: search / save   ·   Ctrl+G: generate   ·   Esc: clear"

COLORS = {
    "info": "#666666",
    "ok": "#2e7d32",
    "error": "#c62828",
    "weak": "#c62828",
    "fair": "#e08600",
    "strong": "#2e7d32",
}

_rng = secrets.SystemRandom()


# ---------------------------- DATA ------------------------------- #
def normalize_website(name):
    return name.strip().lower()


def find_key(data, website):
    """Return the stored key matching website (ignoring case/spaces), or None."""
    target = normalize_website(website)
    for key in data:
        if normalize_website(key) == target:
            return key
    return None


def load_data():
    """Return the saved credentials, or {} if there are none yet.

    Raises ValueError if data.json exists but can't be read as JSON.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as data_file:
            content = data_file.read()
    except FileNotFoundError:
        return {}
    if not content.strip():
        return {}
    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"{DATA_FILE.name} is corrupted: {error}") from error


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)


def load_default_email():
    """Read the default email from config.json (not committed to git)."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            return json.load(config_file).get("default_email", "")
    except (FileNotFoundError, json.JSONDecodeError):
        return ""


# ---------------------------- PASSWORDS ------------------------------- #
def make_password():
    nr_letters = _rng.randint(10, 12)
    nr_numbers = _rng.randint(3, 4)
    nr_symbols = _rng.randint(3, 4)

    password_list = (
        [secrets.choice(string.ascii_letters) for _ in range(nr_letters)]
        + [secrets.choice(string.digits) for _ in range(nr_numbers)]
        + [secrets.choice(SYMBOLS) for _ in range(nr_symbols)]
    )
    _rng.shuffle(password_list)
    return "".join(password_list)


def password_strength(password):
    """Rate a password as "weak", "fair" or "strong" ("" if empty)."""
    if not password:
        return ""
    score = 0
    score += len(password) >= 8
    score += len(password) >= 12
    score += len(password) >= 16
    score += len(password) >= 20
    score += any(c.islower() for c in password) and any(c.isupper() for c in password)
    score += any(c.isdigit() for c in password)
    score += any(not c.isalnum() for c in password)
    if len(password) < 8 or score <= 3:
        return "weak"
    if score <= 4:
        return "fair"
    return "strong"


def mask(password):
    return HIDDEN_CHAR * len(password)


# ---------------------------- UI HELPERS ------------------------------- #
_status_job = None


def set_status(message, kind="info", timeout=STATUS_CLEAR_MS):
    """Show a message in the status bar; it disappears after `timeout` ms (None = stays)."""
    global _status_job
    if _status_job is not None:
        window.after_cancel(_status_job)
        _status_job = None
    status_label.config(text=message, foreground=COLORS[kind])
    if timeout is not None:
        _status_job = window.after(timeout, lambda: set_status(SHORTCUT_HINT, timeout=None))


def copy_to_clipboard(text):
    """Copy text, then clear the clipboard after a delay if it still holds it."""
    pyperclip.copy(text)

    def clear_clipboard():
        if pyperclip.paste() == text:
            pyperclip.copy("")

    window.after(CLIPBOARD_CLEAR_MS, clear_clipboard)


saved_sites = []


def refresh_sites(data):
    saved_sites[:] = sorted(data, key=str.lower)
    website_input["values"] = saved_sites


def filter_sites(event):
    """Narrow the website dropdown to saved sites containing what was typed."""
    if event.keysym in ("Return", "Escape", "Up", "Down", "Tab"):
        return
    typed = normalize_website(website_var.get())
    website_input["values"] = [site for site in saved_sites if typed in normalize_website(site)]


def toggle_password_visibility():
    password_input.config(show="" if show_password_var.get() else HIDDEN_CHAR)


def update_strength(*_):
    level = password_strength(password_var.get())
    if level:
        strength_label.config(text=f"Strength: {level.title()}", foreground=COLORS[level])
    else:
        strength_label.config(text="")


def center_window(win):
    win.update_idletasks()
    width, height = win.winfo_width(), win.winfo_height()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 3
    win.geometry(f"+{x}+{y}")
    win.minsize(width, height)


# ---------------------------- ACTIONS ------------------------------- #
def generate_password(event=None):
    password = make_password()
    password_var.set(password)
    copy_to_clipboard(password)
    set_status("Password generated and copied (clears in 30s).", "ok")


def search_password(event=None):
    website = normalize_website(website_var.get())
    if not website:
        set_status("Enter a website to search for.", "error")
        website_input.focus_set()
        return

    try:
        data = load_data()
    except ValueError as error:
        messagebox.showerror(title="Error", message=str(error))
        return

    key = find_key(data, website)
    if key is None:
        if data:
            set_status(f"No details for {website} exist.", "error")
        else:
            set_status("No passwords saved yet.", "error")
        return

    password = data[key]["password"]
    website_var.set(key)
    email_var.set(data[key]["email"])
    password_var.set(password)
    copy_to_clipboard(password)
    set_status(f"Found {key}. Password copied (clears in 30s).", "ok")


def save_password(event=None):
    website = normalize_website(website_var.get())
    email = email_var.get().strip()
    password = password_var.get()

    if not website or not email or not password:
        set_status("Please don't leave any fields empty.", "error")
        return

    try:
        data = load_data()
    except ValueError as error:
        messagebox.showerror(
            title="Error",
            message=f"{error}\n\nFix or move the file before saving, so existing passwords aren't overwritten.",
        )
        return

    existing_key = find_key(data, website)
    if existing_key is not None:
        is_ok = messagebox.askyesno(
            title="Replace password?",
            message=f"{existing_key} already has a saved password.\n\nReplace it with the new one?",
            icon=messagebox.WARNING,
        )
    else:
        is_ok = messagebox.askyesno(
            title="Save password?",
            message=f"Website: {website}\nEmail: {email}\nPassword: {mask(password)}\n\nSave these details?",
        )
    if not is_ok:
        return

    if existing_key is not None:
        del data[existing_key]
    data[website] = {"email": email, "password": password}
    save_data(data)
    refresh_sites(data)
    clear_form()
    set_status(f"✓ Saved {website}", "ok")


def clear_form(event=None):
    website_var.set("")
    email_var.set(DEFAULT_EMAIL)
    password_var.set("")
    show_password_var.set(False)
    toggle_password_visibility()
    website_input["values"] = saved_sites
    set_status(SHORTCUT_HINT, timeout=None)
    website_input.focus_set()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=24, pady=20)
window.columnconfigure(1, weight=1)
window.resizable(True, False)

image_logo = PhotoImage(file=LOGO_FILE)
window.iconphoto(True, image_logo)

DEFAULT_EMAIL = load_default_email()

website_var = StringVar()
email_var = StringVar(value=DEFAULT_EMAIL)
password_var = StringVar()
show_password_var = BooleanVar(value=False)

ROW_PAD = 4
LABEL_PAD = (0, 8)
BUTTON_PAD = (8, 0)

canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=image_logo)
canvas.grid(row=0, column=0, columnspan=3, pady=(0, 12))

# Website
ttk.Label(text="Website:").grid(row=1, column=0, sticky="e", padx=LABEL_PAD, pady=ROW_PAD)
website_input = ttk.Combobox(textvariable=website_var, width=33)
website_input.grid(row=1, column=1, sticky="ew", pady=ROW_PAD)
search_button = ttk.Button(text="Search", command=search_password)
search_button.grid(row=1, column=2, sticky="ew", padx=BUTTON_PAD, pady=ROW_PAD)

# Email
ttk.Label(text="Email/Username:").grid(row=2, column=0, sticky="e", padx=LABEL_PAD, pady=ROW_PAD)
username_input = ttk.Entry(textvariable=email_var)
username_input.grid(row=2, column=1, columnspan=2, sticky="ew", pady=ROW_PAD)

# Password
ttk.Label(text="Password:").grid(row=3, column=0, sticky="e", padx=LABEL_PAD, pady=ROW_PAD)
password_frame = ttk.Frame(window)
password_frame.grid(row=3, column=1, sticky="ew", pady=ROW_PAD)
password_frame.columnconfigure(0, weight=1)
password_input = ttk.Entry(password_frame, textvariable=password_var, show=HIDDEN_CHAR)
password_input.grid(row=0, column=0, sticky="ew")
show_toggle = ttk.Checkbutton(
    password_frame, text="Show", variable=show_password_var, command=toggle_password_visibility
)
show_toggle.grid(row=0, column=1, padx=(8, 0))
generate_pass_btn = ttk.Button(text="Generate Password", command=generate_password)
generate_pass_btn.grid(row=3, column=2, sticky="ew", padx=BUTTON_PAD, pady=ROW_PAD)

strength_label = ttk.Label(text="")
strength_label.grid(row=4, column=1, sticky="w")

add_button = ttk.Button(text="Add", command=save_password)
add_button.grid(row=5, column=1, columnspan=2, sticky="ew", pady=(8, 0))

# Status bar
ttk.Separator(orient="horizontal").grid(row=6, column=0, columnspan=3, sticky="ew", pady=(16, 6))
status_label = ttk.Label(text="")
status_label.grid(row=7, column=0, columnspan=3, sticky="w")

# Events and keyboard shortcuts
password_var.trace_add("write", update_strength)
website_input.bind("<KeyRelease>", filter_sites)
website_input.bind("<<ComboboxSelected>>", search_password)
website_input.bind("<Return>", search_password)
username_input.bind("<Return>", lambda event: password_input.focus_set())
password_input.bind("<Return>", save_password)
window.bind("<Control-g>", generate_password)
window.bind("<Control-G>", generate_password)
window.bind("<Escape>", clear_form)

# Initial state
set_status(SHORTCUT_HINT, timeout=None)
try:
    refresh_sites(load_data())
except ValueError:
    set_status(f"Can't read {DATA_FILE.name}: the file is corrupted.", "error", timeout=None)

website_input.focus_set()
center_window(window)
window.mainloop()
