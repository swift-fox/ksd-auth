# ksd-auth
Keystroke Dynamics Authentication library.

##What it is
Authenticate the user with not only the password, but also how he/she types it.

The browser-side records the timing pattern when the user types the password. The server-side compares it against previous patterns to authenticate the user.

The timing pattern of a user inputting a password is an unique and relatively inertial characteristic. Making keystroke dynamics an effective identification to distinguish the user from imposters. This library exploits this, making it another dimension of the password and strengthening password-based authentication protocols.

## Try it!

Prerequisite: Python 2.7

1. Checkout the code
2. Start the server with

        ./server.sh

3. Initialize the database at [http://localhost:8000/cgi-bin/user.py](http://localhost:8000/cgi-bin/user.py)
4. Visit the demo page at [http://localhost:8000/demo.html](http://localhost:8000/demo.html)
5. Input a username and type a password. Then click "Create an account"
6. Refresh the page and use the same credential to to login.
