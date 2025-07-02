#!/usr/bin/env python3

import shutil
import sys
import os
import argparse

# more awesome things
#
def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def get_disk_usage(path):
    """Get disk usage statistics for a given path"""
    try:
        total, used, free = shutil.disk_usage(path)
        return total, used, free
    except Exception as e:
        print(f"Error getting disk usage for {path}: {e}", file=sys.stderr)
        return None, None, None

def list_disk_space(paths=None):
    """List disk space for given paths or current directory"""
    if not paths:
        paths = [os.getcwd()]
    
    print(f"{'Path':<20} {'Total':<12} {'Used':<12} {'Free':<12} {'Used%':<8}")
    print("-" * 68)
    
    for path in paths:
        if not os.path.exists(path):
            print(f"Path does not exist: {path}", file=sys.stderr)
            continue
            
        total, used, free = get_disk_usage(path)
        if total is not None:
            used_percent = (used / total) * 100 if total > 0 else 0
            print(f"{path:<20} {format_bytes(total):<12} {format_bytes(used):<12} {format_bytes(free):<12} {used_percent:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='List disk space usage')
    parser.add_argument('paths', nargs='*', help='Paths to check (default: current directory)')
    parser.add_argument('-a', '--all', action='store_true', help='Show all mounted filesystems')
    
    args = parser.parse_args()
    
    if args.all:
        # On Unix-like systems, show common mount points
        if os.name == 'posix':
            mount_points = ['/']
            # Add other common mount points if they exist
            for mp in ['/home', '/var', '/tmp', '/boot']:
                if os.path.ismount(mp):
                    mount_points.append(mp)
            list_disk_space(mount_points)
        else:
            # On Windows, show all drives
            drives = [f"{chr(i)}:\\" for i in range(65, 91) if os.path.exists(f"{chr(i)}:\\")]
            list_disk_space(drives)
    else:
        list_disk_space(args.paths)

if __name__ == '__main__':
    main()
