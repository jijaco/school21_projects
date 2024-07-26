Quickstart
==========

First steps:
    .. code-block:: bash

        python3 -m venv venv
        . venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt

After that you need to paste the token of your bot in tg_bot.py:
    .. code-block:: python

        API_TOKEN = 'your_token'

Now you can start the game:
    .. code-block:: bash

        python3 tg_bot.py
        (pip install --force-reinstall -v "aiogram==2.23.1")