from database.connection import DatabaseManager

db = DatabaseManager()

db.initialize_database()

print("Database initialized successfully.")

db.close()