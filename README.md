# AFOAIC (Accessible Friendly Open AI Chat Client) #

## Introduction ##

AFOAIC is an accessible / screen reader friendly GPT client application written in Python programming language and currently being developed for Microsoft Windows operating system.
AFOAIC is currently pretty much in development, but it already supports basic features such as communicating with GPT4 service, allowing you to use it as your everyday AI assistant. Think of it as ChatGPT that you run locally on your computer.

## Getting started ##

### Obtaining an API key from OpenAI ###

Although AFOAIC application is free, accessing OpenAI APIs such as GPT4 isn't. You need to obtain an API key from OpenAI directly so that AFOAIC can communicate with their APIs. Actually, you get free credits, but it will expire in several months and afterwards you will have to pay for API usage. For normal usage, it should be less than $5 a month.
To obtain an API key, do the following:

1. Go to the following link: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
2. Login or make an account if you don't have one.
3. Locate and press the button "Create new secret key".
4. Launch AFOAIC application, select Chat menu then Options or press Ctrl+Shift+O keyboard shortcut, and then paste your obtained API key in the respective edit box. Then press OK button.


Note, keep your API key in a safe place. You will need it if you ever lose AFOAIC's configuration file where your all settings are locally saved. AFOAIC developers do **NOT** store your personal information such as API key and chat history anywhere except on your local machine. You must take care of your personal data yourself.

### Running from source ###

We are using Python 3.12 for running and building AFOAIC from source, but you shouldn't have a problem if you're running Python 3.11 or Python 3.10 as well.
To prepare Python virtual environment for developing and running AFOAIC from source, do the following:

1. Go to the repository's root directory, then switch to `tools` subdirectory.
2. Run `envprep.bat` batch script that will automatically create Python virtual environment and download required dependencies specified in `requirements.txt` file located in repository's root directory.
3. Run `envrun.bat` batch script to launch AFOAIC from source in a newly prepared virtual environment.


Note: stdin, stdout and stderr are logged into log files located in your user's `%temp%` directory. All other log files, including configs and chatlogs are saved into `data` subfolder where the main AFOAIC executable is located.

### Building AFOAIC binary distribution ###

We are using PyInstaller for building binary distribution. To build AFOAIC, do the following:

1. Switch to repository's root directory.
2. Activate Python virtual environment by typing `.\.venv\scripts\activate` and then press Enter.
3. In a command line, type `pyinstaller afoaic.spec` and press Enter.
4. Wait until it builds, then type `deactivate` to exit virtual environment. Your binary distribution will be located under `dist` subfolder. Launch `afoaic.exe` file to start AFOAIC application.


### Generating translation template for localizing AFOAIC into other languages ###

1. Go to the repository's root directory, then switch to `tools` subdirectory.
2. Run `generate_gettext_template.py` script that will automatically generate Gettext template (afoaic.pot) file for translation under src\locale subfolder.
3. Under src\locale subfolder, create a folder whose name will be a language code for the language you wish to translate AFOAIC to. For example: `de` for german, `es` for spanish, `ru` for russian.
4. Under this language subfolder, create a subfolder named `LC_MESSAGES`.
5. Next, in this `LC_MESSAGES` folder, paste the above generated `afoaic.pot` file and import it into PoEdit and start translating. If it's the first time you are translating AFOAIC, you will probably want to rename generated `afoaic.pot` file from `afoaic.pot` to `afoaic.po`.
6. Finally, when you have finished translating message strings, compile source `afoaic.po` into binary message file `afoaic.mo` so that AFOAIC can read it. You can do this by simply pressing Ctrl+S in PoEdit.

