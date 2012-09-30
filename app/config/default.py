import socket

# no debugging by default - this is overriden in runserver for local dev
DEBUG = ASSETS_DEBUG = False

# override with something sensible
SECRET_KEY = 'SecretKeyForSessionSigning'

# Email address that emails originate from. Make sure it's real, you own it,
# and SPF allows you to send from it.
DEFAULT_MAIL_SENDER = 'vagrant@%s' % socket.getfqdn()

# General email address for admins and errors
ADMIN_RECIPIENTS = ERROR_EMAIL = ['vagrant@localhost']

# Database connection string
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://@/app'

# fetch from live API or use local file for testing
ADAPTIVE_API_DEBUG = False

ADAPTIVE_API_URL = 'http://adaptive-test-api.herokuapp.com/tweets.json'

ADAPTIVE_API_KEYWORDS = ['coke', 'coca-cola', 'diet cola',]

# how often in seconds app allowed to fetch updates from live API
ADAPTIVE_API_RATE_LIMIT = 30

