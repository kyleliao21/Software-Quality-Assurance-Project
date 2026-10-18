// This header file defines the GameStore class, which manages a collection of games available for sale. It provides methods to load games from a file, find a specific game, add new games, and retrieve the list of available games.
#pragma once

#include <string>
#include <vector>
#include "FileManager.h"
#include "Game.h"
using namespace std;

class GameStore {
    public:
        // Asks filemanager to read the games file and keep the result
        bool loadGames(const FileManager& files) { return files.readGames(availableGames); }

        // Finds a game by name and seller's username and returns a pointer to the Game object, or nullptr if not found
        const Game* findGame(const string& name, const string& sellerUsername) const {
            for (const Game& game : availableGames) {
                if (game.getName() == name && game.getSellerUsername() == sellerUsername) {
                    return &game;
                }
            }
            return nullptr;
        }

        // Puts a new game up for sale.
        void addGame(const Game& game) { availableGames.push_back(game); }

        // Returns a reference to the vector of all available games
        const vector<Game>& getGames() const { return availableGames; }

    private:
        vector<Game> availableGames;
};