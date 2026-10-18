// This header file defines the FileManager class, which is responsible for managing file operations related to user accounts and transactions. It provides methods to read user account data from a specified accounts file and populate a vector of User objects.
#pragma once

#include <string>
#include <vector>
#include "Game.h"
#include "User.h"
using namespace std;

class FileManager {
    public:
        // Remembers the names of the accounts, games and transactions files for reading and writing
        FileManager(const string& accountsFile, const string& gamesFile, const string& transactionFile);

        // Reads the accounts file and populates the provided vector with User objects
        bool readAccounts(vector<User>& users) const;

        // Reads the games file and populates the provided vector with Game objects
        bool readGames(vector<Game>& games) const;

        // Writes the end of session marker to the transaction file
        bool writeEndOfSession() const;

    private:
        string accountsFile;
        string gamesFile;
        string transactionFile;
};