echo "1.2"
coverage run --append server.py not_a_config_file > tmp.actual &
sleep 0.5
diff tmp.actual tests/test_arguments/config_file_not_found.out