# Register blueprints here
from .servicedesk.view_servicedesk import bp_servicedesk,bp_rootview

def init_views(app):
    app.register_blueprint(bp_servicedesk)
    app.register_blueprint(bp_rootview)
