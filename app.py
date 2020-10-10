from server import create_app,db
import os

app = create_app()
port = int(os.environ.get("PORT", 5000))
app.run( port=port)