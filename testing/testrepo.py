from database.connection import DatabaseManager
from database.repository import ProcessedEmailRepository

db = DatabaseManager()

repo = ProcessedEmailRepository(db)

repo.initialize_database()

print(repo.count_processed())