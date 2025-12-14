#!/usr/bin/env python3
import argparse
import plistlib
import os
import sys
import shutil
import subprocess

def fail(msg):
    print(f"\n❌ ERROR: {msg}\n")
    sys.exit(1)

def run_cmd(cmd, require_sudo=False):
    if require_sudo:
        cmd = ["sudo"] + cmd
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        fail(f"Command failed: {' '.join(cmd)}")

def ensure_sudo():
    print("🔐 Admin permissions required.")
    try:
        subprocess.check_call(["sudo", "-v"])
    except subprocess.CalledProcessError:
        fail(
            "Sudo authentication failed.\n"
            "➡️  Please rerun XBypasser using a user-writable app location."
        )

def info_plist_path(app_path):
    return os.path.join(app_path, "Contents", "Info.plist")

def get_bundle_id(app_path):
    plist_path = info_plist_path(app_path)
    if not os.path.exists(plist_path):
        fail("Info.plist not found. This does not look like a valid macOS app.")

    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)

    return plist.get("CFBundleIdentifier")

def set_bundle_id(app_path, new_bundle_id):
    plist_path = info_plist_path(app_path)

    with open(plist_path, "rb") as f:
        plist = plistlib.load(f)

    old_bundle_id = plist.get("CFBundleIdentifier", "UNKNOWN")
    plist["CFBundleIdentifier"] = new_bundle_id

    with open(plist_path, "wb") as f:
        plistlib.dump(plist, f)

    print(f"✅ Bundle ID changed:")
    print(f"   {old_bundle_id} → {new_bundle_id}")

def move_app(src, dest_dir, sudo=False):
    dest = os.path.join(dest_dir, os.path.basename(src))
    if os.path.exists(dest):
        fail(f"Destination already exists: {dest}")

    if sudo:
        run_cmd(["mv", src, dest], require_sudo=True)
    else:
        shutil.move(src, dest)

    return dest

def fix_and_resign(app_path):
    print("🧹 Removing extended attributes (xattr)...")
    run_cmd(["xattr", "-cr", app_path], require_sudo=False)

    print("🔏 Re-signing app (ad-hoc)...")
    try:
        run_cmd(["codesign", "-s", "-", "--deep", "--force", app_path])
    except SystemExit:
        fail(
            "codesign failed.\n"
            "➡️  This app may be SIP-protected or a system app.\n"
            "➡️  This failure is EXPECTED for Apple system apps."
        )

def is_system_app(path):
    return path.startswith("/Applications") or path.startswith("/System")

def main():
    parser = argparse.ArgumentParser(
        description="XBypasser — Modify Bundle ID, re-sign, and restore app safely on macOS"
    )
    parser.add_argument("target_app", help="Path to the .app to modify")
    parser.add_argument("-b", "--bundle", help="Set a new Bundle ID")
    parser.add_argument("-c", "--clone", help="Clone Bundle ID from another app")

    args = parser.parse_args()
    target_app = os.path.abspath(args.target_app)

    if not os.path.exists(target_app):
        fail("Target app not found.")

    if args.clone:
        clone_app = os.path.abspath(args.clone)
        if not os.path.exists(clone_app):
            fail("Clone app not found.")
        new_bundle_id = get_bundle_id(clone_app)
        print(f"📋 Cloned Bundle ID: {new_bundle_id}")
    elif args.bundle:
        new_bundle_id = args.bundle
    else:
        fail("You must specify either -b (bundle) or -c (clone).")

    system_app = is_system_app(target_app)
    original_dir = os.path.dirname(target_app)
    home_dir = os.path.expanduser("~")

    if system_app:
        print("⚠️  System app detected.")
        print("⚠️  Moving back to /Applications will require sudo.")
        print("⚠️  SIP-protected apps WILL FAIL (this is expected).")
        ensure_sudo()

    # 1. Modify Bundle ID
    set_bundle_id(target_app, new_bundle_id)

    # 2. Move to Home
    print("📦 Moving app to Home directory...")
    home_app_path = move_app(target_app, home_dir, sudo=system_app)

    # 3. Fix + re-sign
    fix_and_resign(home_app_path)

    # 4. Move back
    print("📍 Restoring app to original location...")
    try:
        final_path = move_app(home_app_path, original_dir, sudo=system_app)
    except SystemExit:
        fail(
            "Failed to restore app to original location.\n"
            "➡️  This usually means SIP protection or insufficient permissions.\n"
            "➡️  The app is currently in your Home folder."
        )

    print("\n🎉 SUCCESS!")
    print(f"✅ App restored to: {final_path}")

if __name__ == "__main__":
    main()
