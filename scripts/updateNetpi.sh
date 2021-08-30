#!/bin/bash

git pull

sudo systemctl restart media-grab-webapp.service
sudo systemctl restart rev-ssh-tunnel-media-grab-webapp.service
