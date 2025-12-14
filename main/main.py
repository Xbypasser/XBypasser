#!/usr/bin/env python3
import argparse
import plistlib
import os
import sys
import shutil
import subprocess

def info_plist_path(app_path):
    return os.path.join(app_path, "Contents", "Info.plist")

def get_bundle_id(app_path):
    plist_path = info_plist_path(app_path)
    if not os.path.exists(plist_path):
        print(f"❌ Info.plist not found: {plist_path}")
        sys.exit(1)

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

def run_cmd(cmd):
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        print(f"❌ Command failed: {' '.join(cmd)}")
        sys.exit(1)

def move_app(src, dest_dir):
    dest = os.path.join(dest_dir, os.path.basename(src))
    if os.path.exists(dest):
        print(f"❌ Destination already exists: {dest}")
        sys.exit(1)

    shutil.move(src, dest)
    return dest

def fix_and_resign(app_path):
    print("🧹 Clearing extended attributes...")
    run_cmd(["xattr", "-cr", app_path])

    print("🔏 Re-signing app (ad-hoc)...")
    run_cmd(["codesign", "-s", "-", "--deep", "--force", app_path])

def main():
    parser = argparse.ArgumentParser(
        description="XBypasser — Modify macOS app Bundle ID, re-sign, and restore location"
    )
    parser.add_argument("target_app", help="Path to the .app to modify")
    parser.add_argument("-b", "--bundle", help="Set a new Bundle ID")
    parser.add_argument("-c", "--clone", help="Clone Bundle ID from another app")

    args = parser.parse_args()

    target_app = os.path.abspath(args.target_app)

    if not os.path.exists(target_app):
        print(f"❌ App not found: {target_app}")
        sys.exit(1)

    if args.clone:
        clone_app = os.path.abspath(args.clone)
        if not os.path.exists(clone_app):
            print(f"❌ Clone app not found: {clone_app}")
            sys.exit(1)
        new_bundle_id = get_bundle_id(clone_app)
        print(f"📋 Cloned Bundle ID: {new_bundle_id}")
    elif args.bundle:
        new_bundle_id = args.bundle
    else:
        print("❌ You must specify either -b (bundle) or -c (clone)")
        sys.exit(1)

    original_dir = os.path.dirname(target_app)
    home_dir = os.path.expanduser("~")

    # 1. Modify bundle ID
    set_bundle_id(target_app, new_bundle_id)

    # 2. Move to home directory
    print("📦 Moving app to Home directory...")
    home_app_path = move_app(target_app, home_dir)

    # 3. Fix + re-sign
    fix_and_resign(home_app_path)

    # 4. Move back
    print("📍 Restoring app to original location...")
    final_path = move_app(home_app_path, original_dir)

    print("🎉 Done!")
    print(f"✅ App restored to: {final_path}")

if __name__ == "__main__":
    main()
