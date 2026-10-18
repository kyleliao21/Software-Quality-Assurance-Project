#include <iostream>
#include "User.h"
using namespace std;

int main() {
    User user("admin01", "AA", 100.0);
    cout << "hello front end" << endl;
    cout << user.getUsername() << " is " << user.getTypeName() << " with credit " << user.getCredit() << endl;
    cout << "isAdmin: " << user.isAdmin() << endl;


    User buyer("buyer01", "BS", 50.0);
    cout << buyer.getUsername() << " isAdmin: " << (buyer.isAdmin() ? "Yes" : "No") << endl;

    return 0;
}
