// This source file implements the FileManager class, which is responsible for managing file operations related to user accounts and transactions. It provides methods to read user account data from a specified accounts file and populate a vector of User objects.
#include "FileManager.h"

#include <cstdlib>
#include <fstream>
using namespace std;

namespace {
    const size_t USERNAME_WIDTH = 15;
    const size_t TYPE_WIDTH = 2;
    const size_t CREDIT_WIDTH = 9;
    // One account line = username + space + type + space + credit = 28 characters
    const size_t ACCOUNT_LINE_WIDTH = USERNAME_WIDTH + 1 + TYPE_WIDTH + 1 + CREDIT_WIDTH;
    const string END_MARKER = "END";

    // Removes spaces and line endings from both ends of a piece of text
    string trim(const string& text) {
        const string whitespace = " \t\r\n";
        size_t first = text.find_first_not_of(whitespace);
        if (first == string::npos) return ""; 
        size_t last = text.find_last_not_of(whitespace);
        return text.substr(first, last - first + 1);
    }
}

FileManager::FileManager(const string& accountsFile, const string& transactionFile) : accountsFile(accountsFile), transactionFile(transactionFile) {}

bool FileManager::readAccounts(vector<User>& users) const {
    // Try to open the accounts file for reading
    ifstream file(accountsFile);
    if (!file) return false;

    users.clear();
    string line;
    // Read the file one line at a time until there are no more lines
    while (getline(file, line)) {
        // The END line means "no more accounts"
        if (trim(line) == END_MARKER) break;
        // Skip lines that are too short to be a real account line
        if (line.size() < ACCOUNT_LINE_WIDTH) continue;

        // Cut the line into its three fields
        string username = trim(line.substr(0, USERNAME_WIDTH));
        string accountType = line.substr(USERNAME_WIDTH + 1, TYPE_WIDTH);
        double credit = atof(line.substr(USERNAME_WIDTH + 1 + TYPE_WIDTH + 1, CREDIT_WIDTH).c_str());

        // Build a User from the three fields and add it to the list
        users.push_back(User(username, accountType, credit));
    }
    return true;
}


bool FileManager::writeEndOfSession() const {
    // Open the transaction file for writing
    ofstream file(transactionFile);
    if (!file) return false;

    // Write the end of session marker
    file << "00 " << string(USERNAME_WIDTH, ' ') << " " << string(TYPE_WIDTH, ' ') << " 000000.00\n";
    return static_cast<bool>(file);
}