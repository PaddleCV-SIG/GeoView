#!/usr/bin/env bash

set -e

pre-commit run --all-files
npx eslint --ext .js,.vue --fix ../frontend/src
