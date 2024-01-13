coverage erase
echo "1.1"
coverage run --append server.py argument1 argument2 > tmp.actual &
sleep 0.5
diff tmp.actual tests/test_arguments/too_many_args.out
