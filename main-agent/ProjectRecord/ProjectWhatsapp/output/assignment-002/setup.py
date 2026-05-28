"""WhatsApp 帳目分析系統 - Setup configuration."""
from setuptools import setup, find_packages


setup(
    name="whatsapp-accounting",
    version="0.1.0",
    description="WhatsApp 對話帳目分析系統",
    author="ProjectWhatsapp",
    python_requires=">=3.9",
    packages=find_packages(),
    install_requires=[
        "pydantic==2.5.0",
        "openpyxl==3.1.2",
        "click==8.1.7",
        "pillow==10.1.0",
        "pytesseract==0.3.10",
        "python-dotenv==1.0.0",
        "pyyaml==6.0.1",
        "openai==1.6.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "whatsapp-accounting=src.main:cli",
        ],
    },
)
