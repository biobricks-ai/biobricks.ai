#!/bin/bash
rm -rf data
rm -rf .dvc/cache
dvc pull -r dev
