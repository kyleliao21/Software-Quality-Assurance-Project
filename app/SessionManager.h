// This header file defines the SessionManager class, which manages user sessions in the system. It keeps track of the currently logged-in user and provides methods to start and end sessions, check login status, and determine if the current user is an admin.
#pragma once

#include "User.h"
using namespace std;

class SessionManager {
    public:
        // Initializes the SessionManager with no user logged in
        SessionManager() : currentUser("", "", 0.0), loggedIn(false) {}

        // Called at login: remember the user and mark them as logged in
        void startSession(const User& user) { currentUser = user; loggedIn = true; }

        // Called at logout: forget the user and go back to "nobody logged in"
        void endSession() { currentUser = User("", "", 0.0); loggedIn = false; }

        bool isLoggedIn() const { return loggedIn; }

        // Returns true if the current user is an admin, false otherwise. If no user is logged in, returns false
        bool isAdmin() const { return loggedIn && currentUser.isAdmin(); }

        const User& getCurrentUser() const { return currentUser; }

    private:
        User currentUser;
        bool loggedIn;      
};