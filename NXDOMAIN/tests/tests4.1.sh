echo "4.1"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send !EXI - saved to buffer"
coverage run --append client.py 1 0

echo "server send T\n"
coverage run --append client.py 2 1

echo "server EXIT"
sleep 0.1
diff tmp.actual tests/test_buffer/buffered_exit.out
