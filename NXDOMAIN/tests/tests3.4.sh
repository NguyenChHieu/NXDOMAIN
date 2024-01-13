echo "3.4"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send !HELLOO"
cat tests/test_command/invalid_command.in | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_command/invalid_command.out
