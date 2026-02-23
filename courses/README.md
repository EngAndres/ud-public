# Courses 

This space has a set of materials for different courses, all focused on teaching _good practices_, _systems thinking approach_, _software development techniques_, all trying to solve _real-world problems_ using __Python__ programming language, and related tools.

- [Courses](#courses)
  - [How to Setup your Python Workspace](#how-to-setup-your-python-workspace)
  - [How to Setup Required Tools](#how-to-setup-required-tools)
    - [Setup Local Git and GitHub Account](#setup-local-git-and-github-account)
      - [Installing Git on Windows](#installing-git-on-windows)
      - [Installing Git on Linux](#installing-git-on-linux)
      - [Setup Git Local Credentials](#setup-git-local-credentials)
      - [Cloning and Working with Repositories](#cloning-and-working-with-repositories)
  - [List of Courses](#list-of-courses)

---

## How to Setup your Python Workspace

It is strongly recommended to work with _Python 3.13.1_. Also, use virtual environments to get the right isolated work environments.

In this sense, tools such as __PyEnv__, __Poetry__, and __PyTest__ will be used in all courses. For more information related to Python, and how to install/setup anything you need, you can go to the [python course](python-for-everyone/README.md).

---

## How to Setup Required Tools

As a computer engineer, you need to know powerful, useful, and state-of-the-art tools in order to give your best in both college and companies. Here, we will start using _git_ and _docker_ to promote teamwork and good collaborative practices.

### Setup Local Git and GitHub Account

Git is a distributed version control system that allows multiple developers to collaborate on a project. It tracks changes to files and allows developers to work on different branches simultaneously. 

Git is important for team collaboration because it enables developers to work on the same codebase without overwriting each other's changes. It allows for easy collaboration, code review, and integration of changes from multiple team members. Git also provides a complete history of changes, making it easier to track and revert to previous versions if needed.

By using Git, teams can work together efficiently, manage code changes effectively, and ensure that everyone is working on the latest version of the code. It promotes transparency, accountability, and seamless integration of work done by different team members.

#### Installing Git on Windows

To install Git on Windows, you can follow these steps:

1. Visit the official Git [website](https://git-scm.com/downloads). Click on the __Download for Windows__ button to download the _Git installer_.
2. Once the download is complete, locate the downloaded file and double-click on it to run the installer.
3. Follow the instructions in the installer wizard. You can choose the default options or customize the installation according to your preferences.
4. During the installation, make __sure to select__ the option to _add Git to your system's PATH environment variable_. This will allow you to use __Git__ from the command line.
5. Complete the installation process by clicking on the __Finish__ button.

#### Installing Git on Linux

To install Git on Linux, you can use the package manager specific to your Linux distribution. Here are the instructions for Ubuntu/Debian:

1. Open a terminal. Run the following command to update the package lists:

```bash
sudo apt update
```

2. Run the following command to install Git:

```bash
sudo apt install git
```

#### Setup Git Local Credentials

Before you clone a repository on your machine, you need to setup your local Git username and email. This information will be used to identify your commits in the repository's history.

To set your Git username, open a terminal or PowerShell window and run the following commands:
```bash
git config --global user.name "Your GitHub Username"
git config --global user.email "your-email-in-github@example.com"
```

If you want to use _SSH_ connection, recommended for secure connections, follow instructions in this [link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

#### Cloning and Working with Repositories

To clone an existing repository and set up your workspace, follow these steps:

**Option 1: Clone an existing repository (recommended for students)**

1. Navigate to the desired location where you want to clone the repository:
```bash
cd /path/to/your/workspace
```

2. Clone the repository:
```bash
git clone https://github.com/username/repository.git
```

3. Navigate into the cloned folder:
```bash
cd repository-name
```

4. Create your development branch:
```bash
git checkout -b your-dev-branch
```

**Option 2: Create a new project with Git (for new projects)**

1. Create and navigate to your project folder:
```bash
mkdir your-project
cd your-project
```

2. Initialize Git and set up the remote repository:
```bash
git init
git remote add origin https://github.com/username/repository.git
```

3. If the remote repository exists and has content, fetch and set up branches:
```bash
git fetch origin
git checkout -b main origin/main
git checkout -b your-dev-branch
```

**Working with branches:**
- Always work on your development branch, not on `main`
- To update your branch with the latest changes:
```bash
git checkout main
git pull origin main
git checkout your-dev-branch
git merge main
```

- To push your changes:
```bash
git add .
git commit -m "Your commit message"
git push origin your-dev-branch
```

---

## List of Courses

Here you will find course materials, including Python notebooks, slides, course definitions, and more. Explore the _courses_ folder for specific content.

Available courses:

1. [Computer Sciences I](computer-sciences-i/README.md): Algorithmic problem-solving, algorithm design, complexity analysis, data structures (linear and tree), and computational efficiency optimization.

2. [Data Analysis Programming](data-analysis-programming/README.md): Data manipulation with Pandas and Polars, ETL processes, descriptive analysis, data visualization, natural language processing, and exploratory data analysis.

3. [Machine Learning](machine-learning/README.md): Advanced machine learning techniques, reinforcement learning fundamentals, generative models, deep learning optimization, online learning, and ML interpretability.

4. [Python for Everyone](python-for-everyone/README.md): Notebooks and examples covering Python basics—conditionals, loops, functions, tuples, lists, strings, dictionaries, files, and exceptions.

5. [Systems Analysis](systems-analysis/README.md): Systems thinking, systems engineering, analysis and design, robust system design, general systems theory paradigms, project management, and systems simulation.

