import setuptools
from os.path import join, dirname


setuptools.setup(
    name="django_bulb_switcher",
    version='0.1',
    packages=["django_bulb_switcher"],
    install_requires=open(join(dirname(__file__), 'requirements.txt')).readlines(),
    author="Bernardo Fontes",
    author_email="bernardoxhc@gmail.com",
    url="https://github.com/berinhard/django-bulb-switcher",
    license="Apache 2.0",
    description="DB-Independent feature toggle for Django",
    keywords="django switcher feature toggle",
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
