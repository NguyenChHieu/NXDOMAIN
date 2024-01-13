echo "2.2"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send co~m"
cat tests/test_normal_behavior/invalid_a.in  | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_normal_behavior/invalid_a.out