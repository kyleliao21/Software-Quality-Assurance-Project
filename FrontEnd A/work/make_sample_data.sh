# Creates small sample files in the current folder (run: bash make_sample_data.sh).
# The spacing matters, so the files are written with printf.

# Old accounts: username(15) type(2) credit(9); last line is END
printf '%-15s %-2s %s\n' admin01 AA 000500.00  fulluser FS 000100.00 \
                         seller01 SS 000050.00 deleteme FS 000020.00 > old_accounts.txt
printf '%-15s %-2s %s\n' END "" 000000.00 >> old_accounts.txt

# Old available games: game name(26) seller(15) price(6); last line is END
printf '%-26s %-15s %s\n' "Stardew Valley" seller01 015.00  "Hades" seller01 024.99 \
                          "GTA V" deleteme 060.00 > old_games.txt
printf '%-26s %-15s %s\n' END "" 000.00 >> old_games.txt

# Old collection: game name(26) owner(15); last line is END
printf '%-26s %-15s\n' "Hades" fulluser > old_collection.txt
printf '%-26s %-15s\n' END "" >> old_collection.txt

# Merged daily transaction file (as written by a Front End)
printf '%s %-15s %-2s %s\n' 01 newplayer FS 000000.00 > merged.atf             # create
printf '%s %-15s %-2s %s\n' 06 newplayer FS 000200.00 >> merged.atf            # add credit 200.00
printf '%s %-26s %-15s %s\n' 03 Portal admin01 009.99 >> merged.atf            # sell
printf '%s %-15s %-2s %s\n' 02 deleteme FS 000020.00 >> merged.atf             # delete
printf '%s %-26s %-15s %-15s %s\n' 04 "Stardew Valley" seller01 fulluser 015.00 >> merged.atf   # buy (not built yet)
printf '%s %-15s %-2s %s\n' 01 fulluser FS 000000.00 >> merged.atf             # create: name already taken
printf '%s %-15s %-2s %s\n' 00 "" "" 000000.00 >> merged.atf                   # end of session