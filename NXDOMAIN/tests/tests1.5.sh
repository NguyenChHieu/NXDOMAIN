echo "1.5"
coverage run --append server.py tests/sample_files/sample_3.conf > tmp.actual &
sleep 0.5
diff tmp.actual tests/test_arguments/conflict_domain.out