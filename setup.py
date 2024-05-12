from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='restdog',
    version='0.2.0',
    description='Python utility that duplicates file modifications over the web via REST API, powered by watchdog.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Lee Talman',
    author_email='leetlmn@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha'
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    py_modules=['restdog'],
    install_requires=[
        'certifi>=2024.0.0',
        'charset-normalizer>=3.3.0',
        'idna>=3.7',
        'logging>=0.4.9.0',
        'requests>=2.31.0',
        'urllib3>=2.2.0',
        'watchdog>=4.0.0',
    ],
    python_requires='>=3.11',
)