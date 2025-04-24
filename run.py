from app import create_app
from db_init import create_database_if_not_exists


app = create_app()

if __name__ == "__main__":
    if create_database_if_not_exists():
        app.run(debug=True)
    else:
        print("❌ Could not start Flask app due to DB connection error.")
