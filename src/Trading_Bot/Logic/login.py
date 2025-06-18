import sqlalchemy as db
# The database will store a user's username, password, P/L, positions

def login(username, password):
    # Connect to the database
    engine = db.create_engine('sqlite:///user_logins.db')
    connection = engine.connect()