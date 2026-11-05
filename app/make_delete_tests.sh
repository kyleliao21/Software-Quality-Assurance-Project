source ./mk_test.sh

mk delete_success <<'EOF'
login
admin01
delete
deleteme
logout
--- terminal
Enter transaction: Enter username: Logged in as admin01.
Enter transaction: Enter username to delete: User deleteme deleted.
Enter transaction: Logged out.
Enter transaction: 
--- transactions
02 deleteme        FS 000020.00
00 admin01         AA 000500.00
EOF

mk delete_fail_1_not_admin <<'EOF'
login
fulluser
delete
logout
--- terminal
Enter transaction: Enter username: Logged in as fulluser.
Enter transaction: Error: Your account type is not permitted to do that.
Enter transaction: Logged out.
Enter transaction: 
--- transactions
00 fulluser        FS 000100.00
EOF

mk delete_fail_2_invalid_user <<'EOF'
login
admin01
delete
nobody
logout
--- terminal
Enter transaction: Enter username: Logged in as admin01.
Enter transaction: Enter username to delete: Error: No such user.
Enter transaction: Logged out.
Enter transaction: 
--- transactions
00 admin01         AA 000500.00
EOF

mk delete_fail_3_current_user <<'EOF'
login
admin01
delete
admin01
logout
--- terminal
Enter transaction: Enter username: Logged in as admin01.
Enter transaction: Enter username to delete: Error: You cannot delete the account you are logged in with.
Enter transaction: Logged out.
Enter transaction: 
--- transactions
00 admin01         AA 000500.00
EOF