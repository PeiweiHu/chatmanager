from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='chatmanager',
    version='0.0.1',
    author="Peiwei Hu",
    author_email='jlu.hpw@foxmail.com',
    description='A tool collection to facilitate the use of ChatGPT API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/PeiweiHu/chatmanager',
    install_requires=[
        'openai',
        'tiktoken',
    ],
    tests_require=[
        'pytest',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires='>=3.8',
)
