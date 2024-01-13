echo "3.1"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
cat tests/test_command/exit.in | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_command/exit.out
