from setuptools import find_packages, setup

setup(
    name='organizer',
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_marshmallow',
        'flask_jwt_extended',
        'flask_cors',
        'sqlalchemy',
        'passlib',
        'marshmallow-sqlalchemy',
    ],
)