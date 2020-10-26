import setuptools

setuptools.setup(
    name='calescador-discord',
    version='0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'calescador-discord=calescador_discord.__main__:main'
        ]
    }
)
