from pathlib import Path

import setuptools

packages = setuptools.find_packages()
print(packages)
setuptools.setup(
    name="exchange",
    version="0.0.1",
    author="Bulygin_Evgeny",
    packages=packages,
    entry_points={
        'console_scripts': [
            "add_default_currencies=exchange.adding_default_currencies:add_default_currencies",
            "start_bot=bot.cli:start_bot",
            "clear_db=exchange.adding_default_currencies:clear_db"
        ]
    }
)
