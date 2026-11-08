# 🔐 Password Manager

A simple desktop **Password Manager** built with **Python** and **Tkinter**. This application allows you to generate secure passwords, save login credentials locally in a JSON file, and quickly search for saved passwords.

## ⬇️ Download (Windows)

**[Download PasswordManager.exe](https://github.com/iamGNU/password_manager/releases/latest)**: no Python or installation needed. Just download it and double-click.

> **"Windows protected your PC" warning?** The app isn't code-signed yet, so Windows SmartScreen doesn't recognise it. Click **More info → Run anyway**.

Your passwords are saved on your computer in `%APPDATA%\PasswordManager\data.json`.

---

## ✨ Features

* 🔑 Generate strong random passwords, with a live strength meter (Weak / Fair / Strong)
* 📋 Automatically copy passwords to the clipboard (cleared after 30 seconds)
* 💾 Save website credentials (website, email/username, password)
* 🔍 Search saved passwords by website, with a dropdown of your saved sites
* 🙈 Password field is hidden by default, with a **Show** toggle
* ⚠️ Warns before overwriting a password that's already saved
* ⌨️ Keyboard shortcuts and a status bar instead of constant pop-ups
* 📂 Store credentials locally in a `data.json` file
* 🖥️ Native-looking GUI built with Tkinter / ttk

---

## 📸 Screenshot

> Screenshot of window where user interact with password manager

![Password Manager Screenshot](assets/Screenshot_main.png)

> Screenshot of saved password file.

![Password Manager Screenshot](assets/Screenshot_savedpass.png)

---

## 🛠️ Technologies Used

* Python 3
* Tkinter
* JSON
* `secrets` (cryptographically secure random generation)
* Pyperclip

---

## 📦 Running from Source (for developers)

If you just want to use the app, grab the [download](#️-download-windows) above instead.

1. Clone the repository:

```bash
git clone https://github.com/iamGNU/password_manager.git
```

2. Navigate to the project folder:

```bash
cd password_manager
```

3. Install the required dependency:

```bash
pip install -r requirements.txt
```

4. (Optional) Set a default email that is pre-filled in the app:

```bash
cp config.example.json config.json
```

Then edit `config.json` and put your email in `default_email`. This file is git-ignored.

5. Run the application:

```bash
python main.py
```

---

## 🚀 How to Use

### 1. Save a Password

* Enter the website name.
* Enter your email or username.
* Click **Generate Password** (or type your own and check the strength meter).
* Click **Add** (or press **Enter** in the password field).
* Confirm the details when prompted. If the website is already saved, you'll be asked whether to replace it.

The credentials will be saved in `data.json`.

---

### 2. Search for a Password

* Type the website name or pick it from the dropdown (the list narrows as you type).
* Click **Search** or press **Enter**.
* Search ignores upper/lower case and extra spaces (`GitHub.com` finds `github.com`).
* If credentials exist, the form is filled in with the saved email and password (tick **Show** to see the password).
* The password is automatically copied to your clipboard, and the clipboard is cleared after 30 seconds.

---

### Keyboard Shortcuts

| Key | Action |
| --- | --- |
| **Enter** in Website | Search |
| **Enter** in Email | Move to the Password field |
| **Enter** in Password | Add / save |
| **Ctrl+G** | Generate a password |
| **Esc** | Clear the form |

---

### 3. Generate a Secure Password

Click **Generate Password** to create a 16–20 character random password containing:

* Uppercase and lowercase letters
* Numbers
* Special characters

Passwords are generated with Python's `secrets` module, which is designed for security-sensitive randomness. The generated password is automatically copied to your clipboard (cleared after 30 seconds).

---

## 📁 Data Storage

All credentials are stored locally in a file named `data.json`:

| How you run it | Where `data.json` (and `config.json`) live |
| --- | --- |
| `PasswordManager.exe` | `%APPDATA%\PasswordManager\` |
| `python main.py` | The project folder |

Set the `PASSWORD_MANAGER_DATA_DIR` environment variable to use a different folder.

**Moving from the Python version to the .exe?** Copy your `data.json` (and `config.json`) from the project folder into `%APPDATA%\PasswordManager\`.

Example:

```json
{
    "github.com": {
        "email": "example@gmail.com",
        "password": "aB8#K2!LmP"
    },
    "google.com": {
        "email": "example@gmail.com",
        "password": "X7$pL9@Q"
    }
}
```

---

## 📋 Requirements

* Python 3.8 or later
* pyperclip

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Building the .exe

```bash
pip install -r requirements-dev.txt
pyinstaller PasswordManager.spec --noconfirm
```

The app is created at `dist/PasswordManager.exe`. To publish it, create a release on GitHub and attach that file:

```bash
gh release create v1.0.0 dist/PasswordManager.exe --title "v1.0.0" --notes "First Windows release"
```

---

## 📂 Project Structure

```text
password_manager/
│
├── main.py               # Main application
├── assets/               # Screenshots and the .exe icon (icon.ico)
├── logo.png              # Application logo
├── PasswordManager.spec  # PyInstaller recipe for building the .exe
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Extra tools for building the .exe
├── config.example.json   # Template for config.json
├── config.json           # Your default email (created by you, git-ignored)
├── data.json             # Saved credentials (created by the app, git-ignored)
└── README.md
```

---

## ⚠️ Notes

* Passwords are stored locally in plain JSON format.
* This project is intended for learning purposes and is **not recommended for storing sensitive credentials** without adding encryption and stronger security measures.
* If `data.json` does not exist, it will be created automatically when you save your first password.
* `data.json` and `config.json` are listed in `.gitignore` so your credentials are never committed. Don't remove them from it.

---

## 🔮 Future Improvements

* Encrypt stored passwords
* Master password authentication
* Dark mode
* Edit and delete saved credentials
* Export and import password database
* macOS and Linux builds

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Akash Anand**

If you found this project helpful, consider giving it a ⭐ on GitHub!
