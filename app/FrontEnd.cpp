// This file implements the FrontEnd class, which manages user interactions, including login, logout, and account management. It uses FileManager for file operations, SessionManager for session handling, and UserStore for managing user data.
#include "FrontEnd.h"
#include <set>
#include <iomanip>
using namespace std;

namespace {
    // Transactions
    const set<string> COMMANDS = {"create", "delete", "sell", "buy", "refund", "addcredit"};

}

// Constructor initializes the FrontEnd with input/output streams and a FileManager for file operations 
FrontEnd::FrontEnd(istream& input, ostream& output, const FileManager& files) : input(input), output(output), files(files) {}


void FrontEnd::run() {
    displayMessage("Games Distribution Front End. Enter a transaction code (type login to begin).");

    string command;
    // Keep reading commands until the input ends
    while (true) {
        output << "Enter transaction: " << flush;

        if (!getline(input, command)) {
            break;
        }

        if (!command.empty() && command.back() == '\r') {
            command.pop_back();
        }

        handleCommand(command);
    }
}

// Decides what to do with command typed by the user
void FrontEnd::handleCommand(const string& command) {
    if (command == "login") {
        handleLogin();
    } else if (command == "logout") {
        handleLogout();
    } else if (!session.isLoggedIn()) {
        displayError("You must log in first.");
    } else if (command == "listaccounts") {
        handleListAccounts();
    } else if (COMMANDS.count(command) > 0) {
        displayError("That transaction is not available yet.");
    } else {
        displayError("Unknown transaction code.");
    }
}

// Handles the login process
void FrontEnd::handleLogin() {
    // Cannont login if already logged in
    if (session.isLoggedIn()) {
        displayError("You are already logged in.");
        return;
    }
    // Load the users from the accounts file
    if (!users.loadUsers(files)) {
        displayError("The user accounts file could not be read.");
        return;
    }

    // Prompt the user for their username
    string username;
    if (!promptForInput("Enter username: ", username)) return;

    // Look up the username in the list of users
    const User* user = users.findUser(username);
    if (user == nullptr) {
        displayError("Unknown username.");
        return;
    }

    // Start a session for the user and display a success message
    session.startSession(*user);
    displayMessage("Logged in as " + user->getUsername() + ".");
}

// Handles the logout process
void FrontEnd::handleLogout() {
    // Logout is only allowed if a user is currently logged in
    if (!session.isLoggedIn()) {
        displayError("You must log in first.");
        return;
    }
    // Write end of session marker to the transaction file and end the session
    if (!files.writeEndOfSession()) {
        displayError("The daily transaction file could not be written.");
    }
    session.endSession();
    displayMessage("Logged out.");
}


void FrontEnd::handleListAccounts() {
    // Only admins are allowed to list accounts
    if (!session.isAdmin()) {
        displayError("Your account type is not permitted to do that.");
        return;
    }

    // Load the users from the accounts file
    displayMessage("Active accounts:");
    output << left << setw(17) << "Username" << setw(15) << "Type" << "Credit\n";

    // Display each user's information in a formatted manner
    for (const User& user : users.getUsers()) {
        output << left << setw(17) << user.getUsername() << setw(15) << user.getTypeName()
               << fixed << setprecision(2) << user.getCredit() << "\n";
    }
    // Display the total number of accounts at the end
    displayMessage(to_string(users.getUsers().size()) + " account(s).");
}


// Helper function for user interaction
bool FrontEnd::promptForInput(const string& message, string& response) {
    output << message << flush;
    bool gotLine = static_cast<bool>(getline(input, response));
    if (gotLine && !response.empty() && response.back() == '\r') response.pop_back();
    return gotLine;
}

// Prints normal output
void FrontEnd::displayMessage(const string& message) { output << message << endl; }

// Prints error output
void FrontEnd::displayError(const string& message) { displayMessage("Error: " + message); }