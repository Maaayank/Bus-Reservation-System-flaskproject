from server import create_app,db

app = create_app()
app.run(port=12845)