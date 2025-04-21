from setuptools import setup, find_packages

setup(
    name="manuscript_reviewer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
        'python-dotenv>=0.19.0',
        'PyPDF2>=3.0.0',
        'langchain>=0.1.0',
        'langchain-community>=0.0.10',
        'typing-extensions>=4.0.0',
        'requests>=2.31.0',
        'python-json-logger>=2.0.0',
        'nougat-ocr>=0.1.0',
        'pdf2image>=1.16.3',
        'pydantic>=2.0.0',
        'pytest>=7.0.0',
        'tqdm>=4.65.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0'
    ],
) 