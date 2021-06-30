from setuptools import setup, find_packages

setup(
    name="ss3dbc",
    version="0.1",
    url="https://github.com/Streamer272/ss3dbc",
    license="none",
    author="Streamer272",
    author_email="daniel.svitan.team7274dev@gmail.com",
    description="Smart SQLite3 Database Controller For Python",
    packages=find_packages(exclude=["test", "venv"]),
    long_description=open('README.md').read(),
    zip_safe=False
)
