from setuptools import setup, find_packages

setup(
    name='django-firebase-auth',
    version='0.0.1',
    url="https://github.com/reef-technologies/django-firebase-auth",
    description='Django Firebase Authentication adapter',
    long_description='TODO',
    author='Reef Technologies',
    author_email='michal.nowacki@reef.pl',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=["firebase_admin~=5.2.0"],
)
