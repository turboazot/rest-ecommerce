import api.app
import flask
import api.extensions
app = api.app.create_app()

@app.cli.command('migrate')
def migrate():
  api.extensions.db.create_all()