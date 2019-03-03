#!/bin/sh
cat $1 | sort -u -k 2 >"sorted_"$1 
