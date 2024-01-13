echo "3.2.2"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send !ADD net hi"
cat tests/test_command/add_invalid_port.in | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_command/add_invalid_port.out
