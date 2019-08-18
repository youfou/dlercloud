import setuptools

with open('README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='dlercloud',
    version='0.0.5',
    author='Youfou',
    author_email='youfouzz@gmail.com',
    description='A Python Wrapper for DlerCloud API',
    keywords=[
        'DlerCloud',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/youfou/dlercloud',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
