from app import create_app
import os
import click
from dotenv import load_dotenv
config_name = os.getenv('FLASK_CONFIG')

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
