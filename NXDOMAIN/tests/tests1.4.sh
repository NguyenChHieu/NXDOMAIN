echo "1.4"
coverage run --append server.py tests/sample_files/sample_2.conf > tmp.actual &
sleep 0.5
diff tmp.actual tests/test_arguments/invalid_domain_found.out
