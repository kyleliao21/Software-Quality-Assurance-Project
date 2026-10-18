// This header file defines the UserStore class, which manages a collection of User objects. It provides methods to load users from a file and find users by their username.
#pragma once

#include <string>
#include <vector>
#include "FileManager.h"
#include "User.h"
using namespace std;

class UserStore {
    public:
        // Asks filemanager to read the accounts file and keep the result
        bool loadUsers(const FileManager& files) { return files.readAccounts(users); }

        // Finds a user by username and returns a pointer to the User object, or nullptr if not found
        const User* findUser(const string& username) const {
            for (const User& user : users) {
                if (user.getUsername() == username) return &user;
            }
            return nullptr;
        }
        
        // Returns a reference to the vector of all users
        const vector<User>& getUsers() const { return users; }

    private:
        vector<User> users;
};