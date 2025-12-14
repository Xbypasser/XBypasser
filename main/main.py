#!/usr/bin/env python3
import argparse
import plistlib
import os
import sys

def get_bundle_id(app_path):
    info_plist_path = os.path.join(app_path, "Contents", "Info.plist")
    if not os.path.exists(info_plist_path):
        print(f"Error: Info.plist not found at {info_plist_path}")
        sys.exit(1)
    with open(info_plist_path, "rb") as f:
        plist = plistlib.load(f)
    return plist.get("CFBundleIdentifier")

def change_bundle_id(app_path, new_bundle_id):
    info_plist_path = os.path.join(app_path, "Contents", "Info.plist")
    with open(info_plist_path, "rb") as f:
        plist = plistlib.load(f)

    old_bundle_id = plist.get("CFBundleIdentifier", "UNKNOWN")
    plist["CFBundleIdentifier"] = new_bundle_id

    with open(info_plist_path, "wb") as f:
        plistlib.dump(plist, f)

    print(f"Changed CFBundleIdentifier from '{old_bundle_id}' to '{new_bundle_id}' for {app_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Modify a macOS app's CFBundleIdentifier in Info.plist"
    )
    parser.add_argument("target_app", type=str, help="Path to the .app folder to modify")
    parser.add_argument("-b", "--bundle", type=str, help="New Bundle ID to set")
    parser.add_argument("-c", "--clone", type=str, help="Path to another .app to copy its Bundle ID")

    args = parser.parse_args()

    if not os.path.exists(args.target_app):
        print(f"Error: Target app does not exist: {args.target_app}")
        sys.exit(1)

    if args.clone:
        if not os.path.exists(args.clone):
            print(f"Error: Clone app does not exist: {args.clone}")
            sys.exit(1)
        new_bundle_id = get_bundle_id(args.clone)
    elif args.bundle:
        new_bundle_id = args.bundle
    else:
        print("Error: Must specify either -b (bundle) or -c (clone). Use -h for help.")
        sys.exit(1)

    change_bundle_id(args.target_app, new_bundle_id)

if __name__ == "__main__":
    main()
