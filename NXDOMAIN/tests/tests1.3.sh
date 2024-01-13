echo "1.3"
coverage run --append server.py tests/sample_files/sample_1.conf > tmp.actual &
sleep 0.5
diff tmp.actual tests/test_arguments/invalid_root.out