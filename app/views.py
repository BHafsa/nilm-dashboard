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

    default_view = '/dashboard'


    @expose('/dashboard/')
    @has_access
    def home(self):
        self.update_redirect()
        return self.render_template('dashboard.html')

    @expose('/history/')
    @has_access
    def home(self):
        self.update_redirect()
        return self.render_template('history.html')

    @expose('/appliance/')
    @has_access
    def home(self, appliance_name, model_name=None):
        """
        This function allows provides an appliance name that need to be disaggregated and the 
        """

        return self.render_template('appliance.html', appliance_name)

appbuilder.add_view(Home, "Home", category='Home')


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
