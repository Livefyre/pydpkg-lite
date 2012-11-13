#!/usr/bin/env python

import os
import sys
import fnmatch
import subprocess
import re


def get_all_debs(path):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.deb'):
            f_path = os.path.join(root, filename)
            matches.append(os.path.relpath(f_path, path))
    return matches


def get_existing_debs(packages_file):
    matches = re.findall(r"Filename:(.*)\n", get_packages_file(packages_file))
    return [match.replace('//', '/').strip() for match in matches]


def get_packages_file(packages_file):
    existing_deb_str = ""
    if os.path.exists(packages_file):
        with open(packages_file, 'r') as f:
            existing_deb_str = f.read()
    return existing_deb_str


def main(root_path, package_file=None):
    all_debs = get_all_debs(root_path)
    existing_debs = []
    output = ""

    if package_file:
        existing_debs = get_existing_debs(package_file)
        output = get_packages_file(package_file)

    for deb in all_debs:
        if deb in existing_debs:
            continue
        full_deb = os.path.join(root_path, deb)
        out = subprocess.check_output(['dpkg-deb', '-I', full_deb, 'control'])
        size = os.stat(full_deb).st_size
        out_formatted = re.sub(r"^(Version: .*$)", r"\1\nFilename: %s\nSize: %s" % (deb, size), out, flags=re.M)
        output += "\n%s" % out_formatted

    print output


def usage():
    print "Usage: dpkg.py <repo_base> [existing_packages_file]"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        package_file = sys.argv[2] if len(sys.argv) > 2 else None
        main(root_path, package_file)
    else:
        usage()
    sys.exit()
