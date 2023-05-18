from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""

from flask_appbuilder import AppBuilder, BaseView, expose, has_access
from app import appbuilder


class Home(BaseView):
    route_base = '/'
    @expose('/dashboard')
    def dashboard(self):
        self.update_redirect()
        return self.render_template('dashboard.html')

    @expose('/history/<string:period>')
    def history(self, period):
        self.update_redirect()
        return self.render_template('history.html')
    
    @expose('/leaderboard')
    def leaderboard(self):
        self.update_redirect()
        return self.render_template('leaderboard.html')
    
    @expose('/forecast')
    def forecast(self):
        self.update_redirect()
        return self.render_template('forecast.html')
    
    @expose('/tips')
    def tips(self):
        self.update_redirect()
        return self.render_template('tips.html')

    @expose('/appliance/<string:appliance_name>')
    def appliance(self, appliance_name, model_name=None):
        """
        This function allows provides an appliance name that need to be disaggregated and the 
        """
        return self.render_template('appliance.html', appliance_name=appliance_name)
    
    

appbuilder.add_view_no_menu(Home())




@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
