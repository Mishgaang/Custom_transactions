#! /usr/bin/env bash
set -e

poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8008
