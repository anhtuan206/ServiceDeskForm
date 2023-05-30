from flask import Flask



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    # View
    ## Import view from views folder
    from .views import init_views
    ## Import view from views folder
    ## Run Init View Function
    init_views(app)
    ## Run Init View Function
    # View
    return app
