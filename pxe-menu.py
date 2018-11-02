#!/usr/bin/env python3

import os

rootDir = ".."

for root, dirs, files in os.walk(rootDir):
    for product in dirs:
        if "Server" not in product:
            continue
        for root, dirs, files in os.walk(os.path.join(root, product)):
            if "x86_64" not in arch:
                continue
            for arch in dirs:
                for root, dirs, files in os.walk(os.path.join(root, arch)):
                    for dvd in dirs:
                        print(os.path.join(root, dvd))
