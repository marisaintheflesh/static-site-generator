#!/usr/bin/env bash

if [[ -d "static_podcasts/" ]]; then
	cd "static_podcasts/"
	git pull origin main
	git lfs fetch
	git lfs checkout
else
	git clone "https://github.com/marisaintheflesh/podcasts.git" "static_podcasts/"
	cd "static_podcasts/"
	git lfs fetch
	git lfs checkout
fi
