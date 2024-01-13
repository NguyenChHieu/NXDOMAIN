#!/bin/bash

# write your own self-testing script at here!
coverage erase
for path in ~/tests/tests*
do
  bash $path
done
# if you need a more detail report: uncomment line 10 and cmt line 11
#coverage html
coverage report -m