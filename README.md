# 112_tp
My term project for 15-112 : Chess

Things to note:
	
	1. The public server on CMU secure is a test feature. 
	I have only tested connection from Wean Hall and not all campus locations
	The public server should be running 24/7
	If you fail to connect, email me at jianzhoc@andrew.cmu.edu 
	and I will try to resolve the issue as soon as I can
	
	2. The public server randomly matches white players with black players. 
	If you want to make sure that you get into the same game as your friend, start your own local server
	
	3. The AI is really slow. I wouldn't recommend you play against it unless 
	you have the equivalent of an 8th gen mobile Intel i7 or above
	
	4. Feel free to report any bugs to jianzhoc@andrew.cmu.edu as well

To set up your own server and play:

    1. Obtain your machine's local IPv4 address, which you will use to host the server. Instructions are below.
	
    2. Navigate to socket_files/server.py, line 17, and paste your local IP address in

    3. Do the same for socket_files/network.py, line 17

    4. Run socket_files/server.py to start up the server. The terminal should read "server started"

    5. VERY IMPORTANT: Open socket_files/chess.py in a new window before you run it! If you run chess.py with the same 
    terminal you just ran server.py with, chess.py will kill the server instance. 
    To do so, press CTRL-K, then O while you are on chess.py (Command-K on Mac OS).

    6. Once you have chess.py open in a new window, run it, choose Multiplayer, and whichever side you want to play as. 
    Whoever you want to play with should simply be able to run chess.py on their end 
    (with the same IPv4 address in their local network.py) and connect with you. 

To connect to my server and play (I promise I won't inject malicious code into your machine):

	1. Navigate to socket_files/network.py, line 17 and confirm that HOST= "172.26.2.71" and PORT=5555
	
	2. Make sure that you are connected to CMU Secure
	
	3. run chess.py and play!

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
