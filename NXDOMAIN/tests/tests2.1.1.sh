echo "2.1.1"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send com"
echo "server send google.com"
echo "server send www.google.com"
cat tests/test_normal_behavior/valid_a.in  | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_normal_behavior/valid_a.out