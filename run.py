from app import create_app, db
from app.models import User, Client, Case

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Client': Client, 'Case': Case}

if __name__ == '__main__':
    app.run(debug=True)
