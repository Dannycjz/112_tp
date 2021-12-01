Project Name: Online Multiplayer Chess with AI

Description: A chess game where users can play with other users who are on the same local network. 
            They can also to choose play with an AI if they don’t have a partner to play with. 

To set up your own server and play:

    1. Obtain your machine's local IPv4 address, which you will use to host the server. Instructions are below.
	
    2. Navigate to chess_game/server.py, line 17, and paste your local IP address in

    3. Do the same for chess_game/network.py, line 17

    4. Run chess_game/server.py to start up the server. The terminal should read "server started"

    5. VERY IMPORTANT: Open chess_game/chess.py in a new window before you run it! If you run chess.py with the same 
    terminal you just ran server.py with, chess.py will kill the server instance. 
    To do so, press CTRL-K, then O while you are on chess.py (Command-K on Mac OS).

    6. Once you have chess.py open in a new window, run it, choose Multiplayer, and whichever side you want to play as. 
    Whoever you want to play with should simply be able to run chess.py on their end 
    (with the same IPv4 address in their local network.py) and connect with you. 

To connect to my server and play (I promise I won't inject malicious code into your machine):

	1. Navigate to chess_game/network.py, line 17 and confirm that HOST= "172.26.2.71" and PORT=5555
	
	2. Make sure that you are connected to CMU Secure
	
	3. run chess_game/chess.py and play!

*How to obtain your local IP address: 

	-Windows: 
        Open a command prompt, type ipconfig, and press enter. Copy the numbers that are labeled "IPv4 adress"
		
	-Mac OS: 
		*Instructions from https://www.macworld.co.uk/how-to/ip-address-3676112/
		Open System Preferences. (Either click the cogs icon in your dock, 
		or hit the Apple logo drop-down menu at the top left of your screen, and then select System Preferences.)
		Click Network (under the Internet & Wireless section).
		Highlight the option in the left-hand bar that has a green dot, 
		then check the information that appears in the pane on the right. It should say Connected at 
		the top; in the smaller text underneath it will tell you what your internal IP address is.
		
	-Linux/Unix:
		You probably know how to get your IP address if you are using Linux

Libraries that need to be installed: 
    -Pygame