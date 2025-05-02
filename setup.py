from setuptools import setup

setup(
    name='lpml',
    version='0.0.0',
    author='itomaAI inc.',
    author_email='ryutaro.yamauchi@itoma.ai',
    description='LPML: LLM Prompting Markup Language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itomaAI/lpml',
    packages=['lpml'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
