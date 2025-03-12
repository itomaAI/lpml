from setuptools import setup, find_packages

setup(
    name='lpml',
    version='0.1.0',
    author='itomaAI inc.',
    author_email='info@itomaai.com',
    description='LPML: LLM Prompting Markup Language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/itomaAI/lpml',  # GitHubリポジトリのURLに置き換えてください
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
