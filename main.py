# how to enable a python virtual envirorment on mac: 'source flask_server/bin/activate'

from website import create_app

# create_app is located in __init__.py 
app = create_app()

# run server by ensuring you are in virtual environment then running main.py
if __name__ == '__main__':
    app.run(debug=True)
