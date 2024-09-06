import time
import random
import subprocess
import datetime

def run_bot():
    while True:
        # Run the bot script
        try:
            subprocess.run(['python3', 'bot.py'])
        except Exception as e:
            print(f"An error occurred while running the bot: {e}. Retrying in one hour.")

        # Calculate the next interval with noise
        base_interval = 3600  # Base time interval of 1 hour (3600 seconds)
        noise = random.randint(-300, 300)  # Noise in seconds (-5 to +5 minutes)
        next_run = base_interval + noise

        # Print next run time for debugging/logging
        print(f"Time now {datetime.datetime.now()} Next run in {next_run // 60} minutes and {next_run % 60} seconds.")

        # Sleep until the next run
        time.sleep(next_run)

if __name__ == "__main__":
    run_bot()
