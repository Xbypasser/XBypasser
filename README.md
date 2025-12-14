# XBypasser

XBypasser is a macOS app that removes screen time restrictions on any non system app.
---

## ⚠️ Important macOS Warnings

* **System apps WILL FAIL**
* Apps located in `/Applications` require **administrator (sudo) access**
* Some apps including chromium based browsers will fail

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
