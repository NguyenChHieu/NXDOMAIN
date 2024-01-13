echo "3.2.1"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send !ADD net 1029"
cat tests/test_command/add_valid.in | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_command/add_valid.out
