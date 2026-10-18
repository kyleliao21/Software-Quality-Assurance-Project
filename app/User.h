// User.h
// One account: username, account type code (AA, FS, BS, SS) and available credit.
#pragma once

#include <string>
using namespace std;

class User {
public:
    User(const string& username, const string& accountType, double credit)
        : username(username), accountType(accountType), credit(credit) {}

    const string& getUsername() const { return username; }
    const string& getAccountType() const { return accountType; }
    double getCredit() const { return credit; }

    bool isAdmin() const { return accountType == "AA"; }

    // readable name of the account type, e.g. "admin" for "AA".
    string getTypeName() const {
        if (accountType == "AA") return "admin";
        if (accountType == "FS") return "full-standard";
        if (accountType == "BS") return "buy-standard";
        if (accountType == "SS") return "sell-standard";
        return "unknown";
    }

private:
    string username;
    string accountType;
    double credit;
};