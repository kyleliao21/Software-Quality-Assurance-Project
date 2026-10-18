// This header file defines the User class, which represents a user in the system with attributes such as username, account type, and credit. It provides methods to access these attributes and determine if the user is an admin.
#pragma once

#include <string>
using namespace std;

class User {
    public:
        // Constructor to initialize a User object with username, account type, and credit
        User(const string& username, const string& accountType, double credit): username(username), accountType(accountType), credit(credit) {}

        // Getters for the User attributes
        const string& getUsername() const { return username; }
        const string& getAccountType() const { return accountType; }
        double getCredit() const { return credit; }

        // Check if the user is an admin based on the account type
        bool isAdmin() const { return accountType == "AA"; }

        // Get the human-readable name of the account type
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