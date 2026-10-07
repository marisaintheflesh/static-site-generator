#!/usr/bin/env bash

if [[ -d "static_podcasts/" ]]; then
	cd "static_podcasts/"
	git pull origin main
else
	git clone "https://github.com/marisaintheflesh/podcasts.git" "static_podcasts/"
fi
