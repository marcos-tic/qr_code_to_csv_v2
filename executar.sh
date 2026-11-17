#!/usr/bin/env bash
cd "$(dirname "$0")"

# Executa o aplicativo portátil autônomo
if [ -f "./CSVExpress" ]; then
    ./CSVExpress "$@"
elif [ -f "./dist/CSVExpress" ]; then
    ./dist/CSVExpress "$@"
else
    python3 main.py "$@"
fi
