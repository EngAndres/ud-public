# System Analysis - Final Project

This is an skeleton for your course project. In this case you must to show different _systems analyst_ skills, I hope.

The idea is to create a personal virtual assistant to handle your personal ___management knowledge system___. So, you must choice a topic of your interest, make a system analysis around this topic, showing this like _complexity_, _components_, _relations_, _chaos_, anything you consider relevant to understand the _topic_ as a whole __system__. Also, think in concepts as _theory of information_, _theory of communication_, _theory of games_, _projet management_, anything which could help you to make a better system definition. Draw _processes_ and _schemas_ to support your system definition.

Then, gather all information you consider useful (define _boundaries_ for your system), and generate _chunks_ of text with very simple but meaningful information and save into one or few _PDF files_.

Your assistent will use an _OpenSource LLM_ from _Mistral-family_ as knowledgement base, and with the documents you could a sort of _fine tunning_ process to provide the agent with your specific _knowledge system_ using _open source_ tools like _LangChain_ and _HuggingFace_.

## How to Use

Next steps should help you to make the better use possible of this skeleton:
1. Create a _python virtual environtment_ for this project.
2. This project is created using _poetry_, so you could add _python dependencies_ just moving in a terminal ath the root of the project (where this _README_ file is allocated), and execute next command:

```[bash]
poetry install
```

3. To run the project, againa in a temrinal in the root of the project, you could use next command:

```[bash]
poetry run run-agent
```