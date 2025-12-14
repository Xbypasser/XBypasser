# XBypasser

XBypasser is a macOS command-line utility that modifies an app’s `CFBundleIdentifier`, clears quarantine/extended attributes, and re-signs the app so it can run after modification.

---

## ⚠️ Important macOS Warnings

* Modifying an app bundle **breaks Apple code signing**
* **SIP-protected system apps WILL FAIL** (this is expected behavior)
* Apps located in `/Applications` may require **administrator (sudo) access** to restore
* Some Apple system apps cannot be modified at all

XBypasser handles these cases gracefully and explains failures clearly.

---

## 📦 Installation

### One-line automatic install (recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/VolcanoExacutor/XBypasser/refs/heads/main/main/install.sh | bash
```

The installer will:

* Ask whether to install for **User** or **Admin (sudo)**
* Automatically fall back to user install if sudo fails
* Install the `XBypasser` command

---

### User Installation

* Installed to:

```text
~/.local/bin/XBypasser
```

If the command is not found, add this to your shell config (`~/.zshrc` or `~/.bashrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Reload your shell:

```bash
source ~/.zshrc
```

---

### Admin Installation

* Installed to:

```text
/usr/local/bin/XBypasser
```

Requires sudo permissions.

---

## 🚀 Usage

### Show help

```bash
XBypasser -h
```

---

### Change an app’s Bundle ID manually

```bash
XBypasser /path/to/App.app -b com.example.newbundleid
```

---

### Clone Bundle ID from another app

```bash
XBypasser /path/to/App.app -c /path/to/OtherApp.app
```

This copies the `CFBundleIdentifier` from `OtherApp.app` and applies it to the target app.

---

## ❌ Common Errors & Explanations

### SIP-Protected App

```
SIP-protected apps WILL FAIL (expected behavior)
```

Some Apple system apps cannot be modified under any circumstances.

---

### Permission Denied / sudo Required

```
Moving back to /Applications requires sudo
```

Run XBypasser with admin permissions or install the app in a user-writable directory.

---

### App Stuck in Home Folder

If restoring fails, the modified app will remain in your Home directory safely.

---

## 🧹 Uninstall

### User install

```bash
rm ~/.local/bin/XBypasser
```

### Admin install

```bash
sudo rm /usr/local/bin/XBypasser
```

---

## 📜 Disclaimer

XBypasser is provided for educational and development purposes only.

You are responsible for complying with Apple’s licensing terms and local laws.

---

## ✅ Example

```bash
XBypasser /Applications/MyApp.app -b com.example.myapp
```

---

Enjoy 🚀
