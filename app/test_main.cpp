#include <iostream>
#include <fstream>
#include "FileManager.h"
using namespace std;

int main() {
    FileManager files("currentaccounts.txt", "availablegames.txt", "gamescollection.txt", "test_records.atf");
    files.startTransactionFile();
    files.writeCreateRecord(User("newuser", "FS", 0.0));
    files.writeDeleteRecord(User("deleteme", "FS", 20.0));
    files.writeSellRecord(Game("Terraria", "seller01", 29.99));
    files.writeBuyRecord(Game("Hades", "seller01", 24.99), "admin01");
    files.writeRefundRecord("buyer01", "seller01", 10.0);
    files.writeAddCreditRecord(User("fulluser", "FS", 100.0), 500.0);
    files.writeEndOfSession(User("admin01", "AA", 1000.0));

    ifstream file("test_records.atf");
    string line;
    while (getline(file, line)) cout << "[" << line << "]" << endl;
    return 0;
}