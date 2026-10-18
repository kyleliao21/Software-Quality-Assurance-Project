// This source file implements the FileManager class, which is responsible for managing file operations related to user accounts and transactions. It provides methods to read user account data from a specified accounts file and populate a vector of User objects.
#include "FileManager.h"

#include <cstdlib>
#include <fstream>
using namespace std;

namespace {
    const size_t USERNAME_WIDTH = 15;
    const size_t TYPE_WIDTH = 2;
    const size_t CREDIT_WIDTH = 9;

    const size_t GAME_NAME_WIDTH = 26;
    const size_t SELLER_USERNAME_WIDTH = 15;
    const size_t PRICE_WIDTH = 6;

    // One account line = username + space + type + space + credit = 28 characters
    const size_t ACCOUNT_LINE_WIDTH = USERNAME_WIDTH + 1 + TYPE_WIDTH + 1 + CREDIT_WIDTH;

    // One game line = name + space + seller + space + price = 49 characters
    const size_t GAME_LINE_WIDTH = GAME_NAME_WIDTH + 1 + SELLER_USERNAME_WIDTH + 1 + PRICE_WIDTH;

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

// Constructor initializes the FileManager with the names of the accounts, games, and transaction files for reading and writing
FileManager::FileManager(const string& accountsFile, const string& gamesFile, const string& transactionFile) : accountsFile(accountsFile), gamesFile(gamesFile), transactionFile(transactionFile) {}

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


bool FileManager::readGames(vector<Game>& games) const {
    // Try to open the games file for reading
    ifstream file(gamesFile);
    if (!file) return false;

    games.clear();
    string line;
    // Read the file one line at a time until there are no more lines
    while (getline(file, line)) {
        // The END line means "no more games"
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (trim(line) == END_MARKER) break;
        if (line.size() < GAME_LINE_WIDTH) continue;

        // Cut the line into its three fields
        size_t priceStart = line.size() - PRICE_WIDTH;
        size_t sellerStart = priceStart - 1 - SELLER_USERNAME_WIDTH;
        string name = trim(line.substr(0, sellerStart));
        string sellerUsername = trim(line.substr(sellerStart, SELLER_USERNAME_WIDTH));
        double price = atof(line.substr(priceStart).c_str());

        // Build a Game from the three fields and add it to the list
        games.push_back(Game(name, sellerUsername, price));
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