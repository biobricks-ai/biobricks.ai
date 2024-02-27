#!/bin/bash
rm -rf brick
rm -rf .dvc/cache
dvc pull -r dev
