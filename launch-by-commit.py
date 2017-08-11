#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import tempfile
import subprocess
import urllib.request
import zipfile
from os import path

OPENRCT2_VERSIONS = ["0.1.2", "0.1.1", "0.1.0", "0.0.8", "0.0.7", "0.0.6", "0.0.5", "0.0.4", "0.0.3", "0.0.2", "0.0.1"]

OPENRCT2_ORG_URLS = {"windows":"http://cdn.limetric.com/games/openrct2/{0}/develop/{1}/6/OpenRCT2-{0}-develop-{1}-windows-x64.zip",
                     "macos": "",
                     "linux": ""}

EXE_NAMES = {"windows": "openrct2.exe",
             "macos": "",
             "linux:": "openrct2"}

parser = argparse.ArgumentParser(description='OpenRCT2 launch-by-commit-hash helper script.')
parser.add_argument('commit_hash', type=str, nargs=1)
args = parser.parse_args()

commit_hash = args.commit_hash[0].strip()[:7]

if commit_hash == "":
    print("Please provide a commit hash (e.g. 60f02ad)")

platform = "windows"

file_name = None
for version in OPENRCT2_VERSIONS:
	try:
		url = OPENRCT2_ORG_URLS[platform].format(version, commit_hash)
		file_name, headers = urllib.request.urlretrieve(url)
		break
	except urllib.error.HTTPError:
		continue

if file_name is not None:
	with tempfile.TemporaryDirectory() as temp_dir:
		temp_path = path.join(temp_dir, commit_hash)
		with zipfile.ZipFile(file_name, "r") as zip_ref:
			zip_ref.extractall(temp_path)
			subprocess.run([path.join(temp_path, EXE_NAMES[platform])])
