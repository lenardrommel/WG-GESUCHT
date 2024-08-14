# Welcome to WG-Gesucht Bot

This bot automatically updates your listings on WG-Gesucht. It handles the login process, clicks the necessary buttons, and ensures your offers remain up-to-date.


## Installation and Prerequisites

### Install firefox
#### For Mac:
* Open up a new terminal
* run the following command
```sybase
brew upgrade
brew install firefox
```
* Or go to your browser and install [Firefox](https://www.mozilla.org/de/firefox/download/thanks/).

#### For Windows:
* Please consult a therapist

### Install geckodriver
Then you have to install [geckodriver](https://github.com/mozilla/geckodriver/releases).
#### For Linux/Ubuntu:
```sybase
sudo apt install firefox-geckodriver
```

#### For Mac:
```sybase
brew install geckodriver
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/wg-gesucht-auto-updater.git
    cd wg-gesucht-auto-updater
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `config.json` file in the root of the project directory with your WG-Gesucht login credentials:

    ```json
    {
      "email": "your_email@example.com",
      "password": "your_password"
    }
    ```

## Usage

You can run the script as follows:

```bash
python main.py
```
If you want to debug the script, you can run it with the `--debug` flag:

```bash
python main.py --debug
```