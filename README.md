SunComm Signal Fetcher
I created this to help aim the antennas. 
This repository contains a Flask application designed to fetch signal data from a device, given the proper credentials.

These modems go by several different names. Chester Cheetah is one of them. This uses standard AT+ commands as well as the admin @192.168.100.1 to pull signal data.
Upon running this it will ask you for the password for the admin. 

Prerequisites
Python: The script requires Python 3, preferably Python 3.7 or newer.
Git: If you're cloning the repository directly from GitHub, you'll need Git.
Getting Started

1. Clone the Repository
git clone https://github.com/itsmebcc/suncomm.git
cd suncomm

2. Set Up the Environment
It's recommended to use a virtual environment to avoid potential conflicts with other Python packages:

# Install virtualenv if you haven't
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install flask requests

3. Run the Script
Start the Flask application with the following command:

python3 backend.py

When prompted, enter the web admin password.

4. Access the Application
Open a web browser and navigate to:

http://localhost:5000/
To retrieve the signal data, visit:

http://localhost:5000/data

5. Shutting Down
To stop the Flask server, simply go back to your terminal and press CTRL+C.

Afterwards, you can deactivate your virtual environment:

bash
Copy code
deactivate
Issues & Contributions
For issues, please use the GitHub issues section. If you'd like to contribute to the project, feel free to fork the repository and submit a pull request!

License
This project is open source. Check the LICENSE file for more details.
