import argparse
import time

from dogs.dogs_app import TelegramAccount
import os
import logging
import glob
import re
import yaml


def main():
    config = yaml.safe_load(open('config.yaml'))
    logger = logging.getLogger('my_logger')
    logging.basicConfig(level=logging.WARNING,  # Set the logging level
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of the log messages
                        datefmt='%Y-%m-%d %H:%M:%S',  # Date format
                        handlers=[logging.StreamHandler()])  # Log to the console

    parser = argparse.ArgumentParser(description="CLI tool to claim dogs token in telegram")
    parser.add_argument("-a", "--add", type=int, required=False, help="Telegram bot token")

    list_of_files = glob.glob('sessions/*.json')
    args = parser.parse_args()
    if args.add:
        # Log into new accounts
        for i in range(args.add):
            if len(list_of_files) == 0:
                number = 1
            else:
                latest_file = max(list_of_files, key=os.path.getmtime)
                regex = re.compile("ac([0-9]*)")
                number = int(regex.findall(latest_file)[0]) + 1
            acc = TelegramAccount("ac" + str(number), config['proxy'])
            acc.close()
    else:
        # Claim on all accounts in sessions folder
        for filename in list_of_files:
            regex = re.compile("(ac[0-9]*)")
            account = regex.findall(filename)[0]
            acc = TelegramAccount(account, config['proxy'])
            try:
                acc.claim_dogs()
                # print(acc.get_proxy("271cf1c7badd56ab154bd6549ff3acc9"))
            except Exception as E:
                print(str(E))
                logger.critical(f"Failed to claim on {account}")
                acc.close()
                continue
            time.sleep(10)
            acc.close()


if __name__ == '__main__':
    main()
