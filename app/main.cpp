// Games Distribution Front End
// Group 26 - Verify Games

// INPUT: current_accounts.txt, available_games.txt
// OUTPUT: daily_transaction.txt
// RUN: ./FrontEnd
#include <iostream>
#include "FileManager.h"
#include "FrontEnd.h"
using namespace std;

int main(int argc, char* argv[]) {
    // Determine the file names for accounts, games, and transactions based on command line arguments or use default values 
    string accountsFile = (argc > 1) ? argv[1] : "current_accounts.txt";
    string gamesFile = (argc > 2) ? argv[2] : "available_games.txt";
    string transactionFile = (argc > 3) ? argv[3] : "daily_transaction.txt";

    FileManager files(accountsFile, gamesFile, transactionFile);
    FrontEnd frontEnd(cin, cout, files);
    frontEnd.run();
    return 0;
}