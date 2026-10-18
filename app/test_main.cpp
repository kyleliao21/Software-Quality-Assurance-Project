#include <iostream>
#include "FileManager.h"
#include "GameStore.h"
using namespace std;

int main() {
    FileManager files("current_accounts.txt", "available_games.txt", "daily_transaction.txt");
    GameStore games;
    if (!games.loadGames(files)) {
        cout << "Could not read the games file" << endl;
        return 1;
    }
    cout << games.getGames().size() << " games loaded" << endl;

    const Game* found = games.findGame("Minecraft", "seller01");
    cout << "Minecraft by seller01: " << (found ? "found" : "not found") << endl;

    const Game* wrongSeller = games.findGame("Minecraft", "admin01");
    cout << "Minecraft by admin01: " << (wrongSeller ? "found" : "not found") << endl;

    games.addGame(Game("Spiderman", "admin01", 9.99));
    cout << games.getGames().size() << " games after adding Spiderman" << endl;
    return 0;
}