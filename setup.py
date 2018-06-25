from setuptools import setup

setup(name='medapi',
      version='1.0',
      description='Medapi on openshift',
      author='ks',
      author_email='not yet',
      url='https://www.python.org/community/sigs/current/distutils-sig',
      install_requires=['Flask>=0.7.2', 'MarkupSafe', 'pylibmc==1.2.3', 'iron_cache', 'gunicorn', 'flask_restful'],
      )