#include <iostream>
#include "FileManager.h"
#include "FrontEnd.h"
using namespace std;

int main() {
    FileManager files("current_accounts.txt", "daily_transaction.txt");
    FrontEnd frontEnd(cin, cout, files);
    frontEnd.run();
    return 0;
}