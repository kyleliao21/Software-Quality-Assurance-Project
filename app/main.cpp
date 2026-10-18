// Games Distribution Front End
// Group 26 - Verify Games

// RUN: ./FrontEnd
#include <iostream>
#include "FileManager.h"
#include "FrontEnd.h"
using namespace std;

int main(int argc, char* argv[]) {

    string accountsFile = (argc > 1) ? argv[1] : "current_accounts.txt";
    string transactionFile = (argc > 2) ? argv[2] : "daily_transaction.txt";
    FileManager files(accountsFile, transactionFile);
    FrontEnd frontEnd(cin, cout, files);
    frontEnd.run();
    return 0;
}