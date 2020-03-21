#! /bin/bash
WEBEXPE_LANG=fr make stop 
WEBEXPE_LANG=en make stop 
WEBEXPE_LANG=fr make remove
WEBEXPE_LANG=en make remove
make clean

git pull origin master
cp expe/config.expe.py expe/config.py
make build

WEBEXPE_PREFIX_URL=expe2 PORT=8001 WEBEXPE_LANG=fr make run &
WEBEXPE_PREFIX_URL=expe1 PORT=8000 WEBEXPE_LANG=en make run &