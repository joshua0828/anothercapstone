# Group 1 Capstone

## Setup & Installtion

clone this repository to a local repository 
```bash
cd whatever/folder
git clone https://github.com/amgosek/capstone
```

Create Python virtual environment:
```bash
macOS
virtualenv -p python3 path/to/virenv_name
```
I put mine inside of the folder that holds this github repository so there was no path in my case the command looked like this:
```bash
macOS
virtualenv -p python3 server
```
enable virtual environment:
```bash
macOS
source <desired-path>/bin/activate
```
in my case:
```bash
source server/bin/activate
```

install requirements: (you can include path before requirements.txt (path/to/requirements.txt) if you need to)
```bash
pip3 install -r requirements.txt
```

## note

anything over python 3.6 and under 3.10 should work (I'm using 3.8.5). Make sure you have it set as project interrupter! If you run these commands inside of vscode terminal after cloning from this repository a message should pop up asking if youd like to use the virtual environment created.

## Running The App (Might have to run twice to work after initial setup)

```bash
python main.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`


