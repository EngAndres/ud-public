# Python for Everyone

This is just a set of contents in order to provide you some examples and simple explanations about python _syntaxis_ and useful capabilities you could use to develop your academic (and non-academic) projects.

Table of Contents:

- [Python for Everyone](#python-for-everyone)
  - [Notebooks Distribution](#notebooks-distribution)
  - [How to Setup Python on your Machine](#how-to-setup-python-on-your-machine)
    - [Installing Python](#installing-python)
      - [Windows](#windows)
      - [UNIX Systems](#unix-systems)
    - [Creating Virtual Environments](#creating-virtual-environments)
    - ["Pimp" your VS Code (Optional)](#pimp-your-vs-code-optional)


## Notebooks Distribution

To make it simple, _Jupyter Notebooks_ are used to explain the concepts, so it is a good idea to get familiar with notebook usage.

As follows, it is presented the recommended order to explore the notebooks:

1. [Conditionals](conditionals.ipynb) - On Construction
2. [Loops](loops.ipynb) - On Construction
3. [Functions](functions.ipynb)
4. [Tuples](tuples.ipynb)
4. [Lists](lists.ipynb) - On Construction
4. [Strings](strings.ipynb)
5. [Dictionaties](dictionaries.ipynb) - On Construction
4. [Files](files.ipynb) - On Construction
4. [Exceptions](exceptions.ipynb) - On Construction

_You can check any notebook at any time you need, the recommendation is not a mandatory path._

## How to Setup Python on your Machine

The courses are built around _python_, so it is pretty important to have _python_ installed and tunned in your machine. 

### Installing Python

#### Windows
To install Python on your Windows machine, follow these steps:

1. Visit the official Python website at [python.org](https://www.python.org/downloads/). 
2. Click on the _Downloads_ tab. Scroll down to the __Python Releases for Windows__ section, and choose the version of Python you want to install. It is recommended to select the _latest stable version_. However, these courses are built using _Python 3.11.0_.
3. Click on the download link for the Windows installer corresponding to your system architecture (32-bit or _64-bit_ probably). Once the installer is downloaded, double-click on it to start the installation process.
7. In the installer, select the option to __Add Python to PATH__ and click on _Install Now_. ___If you forget this step, _Windows_ will not execute _python_ when you need it___.
8. The installer will now install Python on your machine. This may take a few minutes.
9. Once the installation is complete, you can verify that Python is installed by opening the command prompt, I recommend to use __PowerShell__,  and typing `python --version`. You should see the version number of Python printed on the screen.

Congratulations! You have successfully installed Python on your Windows machine.

#### UNIX Systems

For UNIX Systems, as Linux and MacOS, __python__ is installed by default.

***

### Creating Virtual Environments

There are different tools to create virtual environments, but I use _PyEnv_, it is simple and lets to create virtual environments on different python versions, it is amazing. You could check a good tutorial [https://realpython.com/intro-to-pyenv/](here).

1. Open a _Terminal_ linux or _PowerShell_ window.

2. Install __PyEnv__ by running the following command:
```[bash]
curl https://pyenv.run | bash
```
This will download and install PyEnv on your system.

3. Add __PyEnv__ to your system's _PATH_ by running the following command:
```[bash]
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```
This will ensure that _PyEnv_ is available in _Terminal linux_ or _PowerShell windows_.

4. Restart your _Terminal_ or _PowerShell window_ to apply the changes to your __PATH__.

5. Install _Python 3.11.0_ using __PyEnv__ by running the following command:

```[bash]
pyenv install 3.11.0
```

This will download and install Python 3.11.0 on your environments, but this installation does not affect the _python_ version you have globally in your operative system. In this way, you could install a lot of different _python version_ in your machine without any problem.

6. Create a virtual environment using Python 3.11.0 by running the following command:

```[bash]
pyenv virtualenv 3.11.0 <env_name>
```
Replace ___<env_name>___ with the desired name for your virtual environment.

7. Activate the virtual environment by running the following command:
```[bash]
pyenv activate <env_name>
```
Replace <___env_name>___ with the name of your virtual environment.


Congratulations! You have successfully created a virtual environment using __PyEnv__ and installed __Python 3.11.0__ on your machine.


***

### "Pimp" your VS Code (Optional) 

There are a lot of different _Integrated Development Environment (IDE)_, however I recommend to use _VS Code_. This one is _FOSS_, with a lot of updates, extensions, support different programming languages, simple to use and setup.

To install extensions in VS Code, follow these steps:

1. Open _VS Code_. Click on the __Extensions__ icon on the left sidebar, or press _Ctrl+Shift+X_ (_Cmd+Shift+X_ on macOS) to open the __Extensions__ view.
2. In the search bar at the top of the Extensions view, type the name of the extension you want to install.
3. From the search results, click on the _extension_ you want to install.
On the _extension_ page, click on the __Install__ button. Wait for the installation to complete. You will see a notification once the installation is finished.
4. After the installation, you may need to reload _VS Code_ for the extension to take effect. You can do this by clicking on the _Reload_ button in the notification, or by restarting _VS Code_.
5. That's it! The __extension__ is now installed and ready to use in _VS Code_. You can manage your installed extensions by clicking on the __Extensions__ icon and accessing the _Installed_ tab.

Also, I strongly recommend you to install next extensions:
- __Python__: Code colors, syntax validations
- __Pylint__: Verification of code quality
- __Jupyter__: Notebooks into IDE
- __BlackFormatter__: Format python code
- __isort__ [maybe]: Organize _imports_ order.
- __Docker__: Containers management.
- __DevContainers__: See containers content.
- __GitLens__: Handle git commits, changes, among others.
- __TODO__ Tree: Task to do in the code.
- __LaTeX__: Write and build LaTeX documents.
- __Postman__: Call web APIs.