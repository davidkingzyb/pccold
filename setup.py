# 2019/2/13 by DKZ

from setuptools import setup

setup(name='pccold',
    version='0.1',
    packages=['lib'],
    author='davidkingzyb',
    author_email='davidkingzyb@qq.com',
    license='MIT',
    url='https://pypi.python.org/pypi',
    data_files = [('etc', ['etc/pccold.conf'])],
    keywords="douyu pccold",
    install_requires=[
        'streamlink>=1.0.0',
        'bypy>=1.6.4',
        'psutil>=5.5.0'
    ],
    scripts=['bin/pccold']
    )

# $ python3 setup.py sdist

# $ python3 setup.py sdist bdist_wheel
# $ twine upload dist/pccold-0.1-py3-none-any.whl 