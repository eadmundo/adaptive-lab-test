import os
import simplejson as json
import shutil
from flask.ext.assets import Environment, Bundle, ExternalAssets

assets = Environment()


def configure_assets(app):
    """
    Configures asset Environment.
    """

    # webassets seems to require the environment to be bound to an application
    # before you can change the environment options.
    assets.app = app

    # Configure assets Environment
    assets.versions = 'hash'
    assets.manifest = 'file://%s' % os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/assets/.static-manifest'))
    assets.cache = False
    assets.autobuild = assets.debug
    assets.url = app.config.get('CDN_URL')

    # Build main css bundle
    assets.register('css_main',
        Bundle(
            'css/default.css',
            'css/bootstrap.css',
            filters='cssmin',
        ),
        filters='cssrewrite',
        output='assets/css/main%(version)s.css',
    )

    # paths for bower bundle
    bower_file = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/assets/tmp/bower-paths.json'))
    f = open(bower_file)
    bower_paths = ['assets/%s' % path for path in json.loads(f.read()).values()]

    assets.register('js_main', Bundle(
        Bundle(*bower_paths),
        'assets/tmp/mustache-compiled-templates.min.js',
        Bundle(
            'js/default.js',
            filters='jsmin'
        ),
        output='assets/js/main.%(version)s.js'
    ))

    # Trigger a build of the css_main bundle now, so that we can use it in
    # another bundle later if we want.
    assets['css_main'].urls()

    assets.register_externals(ExternalAssets(['img/*',]))
    assets.config['external_assets_output_folder'] = 'assets/files/'
    app.jinja_env.globals['webasset'] = assets.external_assets.url
