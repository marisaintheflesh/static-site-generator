#!/usr/bin/env bash

if [ -d "__site/" ]; then
	cd __site/
	python3 -m http.server
else
	echo "Static site not currently generated. Did you run mksite.sh?"
fi
