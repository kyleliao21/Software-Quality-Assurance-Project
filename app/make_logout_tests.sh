source ./mk_test.sh

mk logout_success <<'EOF'
login
fulluser
logout
--- terminal
Enter transaction: Enter username: Logged in as fulluser.
Enter transaction: Logged out.
Enter transaction: 
--- transactions
00 fulluser        FS 000100.00
EOF

mk logout_fail_1_not_logged_in <<'EOF'
logout
--- terminal
Enter transaction: Error: You must log in first.
Enter transaction: 
EOF