from sqlalchemy import create_engine
from database import db

# Replace 'your_database_name.db' with the desired name for your SQLite database file
database_file = 'db_directory/gs.db'

# Create the engine to connect to the SQLite database file
engine = create_engine('sqlite:///' + database_file)

# Bind the SQLAlchemy models to the engine
db.init_app(engine)
db.create_all()

