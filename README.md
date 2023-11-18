# Real-Estate-Scraper

## Setup

Installing chrome driver:

```bash 
brew install chromedriver 
```

Getting installation path:

```bash 
which chromedriver
```

If seeing error "Google Chrome for Testing.app” is damaged and can’t be opened. You should move it to the Trash.":

```bash
xattr -cr 'Google Chrome for Testing.app'
```

Setting up .env file:

```
pip install python-dotenv 
```

Define the following variable in your .env file. Add your installation path.

```
CHROMEDRIVER_PATH=YOUR_INSTALLATION_PATH
```