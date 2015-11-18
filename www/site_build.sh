#!/bin/bash
set -eux

# These directories are empty, so git does not check them in
# therefore, make sure they exist
mkdir -p content
mkdir -p layouts

hugo --theme=hugo-creative-theme --verbose

