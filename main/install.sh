#!/bin/bash
set -e

APP_NAME="XBypasser"
RAW_URL="https://raw.githubusercontent.com/VolcanoExacutor/XBypasser/main/main/main.py"

USER_BIN="$HOME/.local/bin"
ADMIN_BIN="/usr/local/bin"

echo "=== $APP_NAME Installer ==="
echo

echo "Choose installation type:"
echo "1) Admin install (requires sudo) → $ADMIN_BIN"
echo "2) User install (no sudo) → $USER_BIN"
echo

# Read from the terminal even when piped via curl
echo -n "Enter choice [1/2]: "
read choice </dev/tty
echo

install_user() {
  echo "Installing $APP_NAME for current user..."

  mkdir -p "$USER_BIN"
  curl -fsSL "$RAW_URL" -o "$USER_BIN/$APP_NAME"
  chmod +x "$USER_BIN/$APP_NAME"

  echo
  echo "✅ Installed to $USER_BIN/$APP_NAME"
  echo
  echo "⚠️ If the command is not found, add this to your shell config:"
  echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
}

install_admin() {
  echo "Installing $APP_NAME system-wide (sudo required)..."
  echo

  if ! sudo -v; then
    echo "❌ Sudo authentication failed."
    echo "➡️  Falling back to user installation."
    echo
    install_user
    return
  fi

  sudo curl -fsSL "$RAW_URL" -o "$ADMIN_BIN/$APP_NAME"
  sudo chmod +x "$ADMIN_BIN/$APP_NAME"

  echo
  echo "✅ Installed to $ADMIN_BIN/$APP_NAME"
}

case "$choice" in
  1)
    install_admin
    ;;
  2)
    install_user
    ;;
  *)
    echo "❌ Invalid choice."
    exit 1
    ;;
esac

echo
echo "🎉 Installation complete."
echo "Run with: $APP_NAME"
