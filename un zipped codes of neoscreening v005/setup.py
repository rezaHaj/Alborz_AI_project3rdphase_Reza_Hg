from setuptools import setup, find_packages
setup(
    name="neo_screenbot",
    version="0.0.5",
    packages=find_packages(),
    install_requires=["streamlit","pandas","numpy","reportlab"],
    author="reza hg",
    author_email="reza.ai.developer@gmail.com",
    description="NeoScreenBot: CH & PKU newborn screening assistant",
)
