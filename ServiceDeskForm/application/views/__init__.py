# Register blueprints here
from .servicedesk.view_servicedesk import bp_servicedesk

def init_views(app):
    app.register_blueprint(bp_servicedesk)
