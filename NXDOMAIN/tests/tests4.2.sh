echo "4.2"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send abc\nbcd\n!EXI"

coverage run --append client.py 3 1
echo "server send T\n"
coverage run --append client.py 2 1
sleep 0.1
diff tmp.actual tests/test_buffer/interrupted_msgs.out
