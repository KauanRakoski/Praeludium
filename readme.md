## Praeludium

![logo](./assets/praeludium_logo.png)

### Setup
To setup run setup.ps1 (powershell), it will create a virtual environment and install the dependencies.


### Running the app
With dependencies already installed, open activate the environment and run main:

```sh
env\Scripts\activate
python main.py
```

This will open the flet application frontend


### Building the app

The app can be build using
```
pip install pyinstaller
flet pack main.py --name Praeludium --hidden-import mido.backends.portmidi --hidden-import pygame._view
```

Needs more testing.