# Pyweek Pirates Project

## Setup 
Clone the repository  
`git clone https://github.com/n0remac/Pyweek.git`  

Create virtual environment  
`python3.7 -m venv Pyweek/venv`  

Enter directory and start virtual environment  
`cd Pyweek && source venv/bin/activate`  

Install dependencies  
`pip install -r requirements.txt`

Run the game! 
`python run_game.py`

### Dependencies
All dependencies for this project are located in the `requirements.txt` file

### Build Installer
To create a binary, use `pyinstaller`

Install pyinstaller:
`pip install pyinstaller`

Tell it to package the game:
`pyinstaller run_game.spec`
