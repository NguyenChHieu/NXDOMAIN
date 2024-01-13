echo "2.4"

coverage run --append server.py tests/sample_files/sample.conf > tmp.actual &
echo "server running"
sleep 1
echo "server send .example..google.com"
echo "server send .com."
echo "server send ex~ample.google.com"
echo "server send example.go~ogle.com"
echo "server send example.google.c~om"
cat tests/test_normal_behavior/invalid_c_b_a.in  | ncat localhost 1024
echo "server send !EXIT"
sleep 0.1
diff tmp.actual tests/test_normal_behavior/invalid_c_b_a.out