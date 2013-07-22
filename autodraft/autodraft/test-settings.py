from autodraft.settings import *
 
ROOT_URLCONF = 'autodraft.settings.test.urls'
 
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ':memory:'
 
INSTALLED_APPS += ('django_nose', )
TEST_RUNER = 'django_nose.NoseTestSuiteRunner'
