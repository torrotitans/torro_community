#!/usr/bin/env bash

cd server
npm install
npm run build:PROD -- REACT_APP_API_URL=$1