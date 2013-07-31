import argparse
import logging
import json

from rectangler import Rectangler


def parse_config(path):
    config_dict = None
    with open(path, "r+") as config_file:
        config_dict = json.load(config_file)
    return config_dict


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--config", help="JSON config file",
                            type=str)
    arg_parser.add_argument("--config-help", help="Config file keys.",
                            action="store_true", dest="config_help")
    arg_parser.add_argument("-v", "--verbose", help="Set logger to DEBUG.",
                            action="store_true")
    arg_parser.add_argument("-i", "--init", help="Initialize project "
                            "(for first run).", action="store_true")
    arg_parser.add_argument("-s", "--scheduled", help="Used when tiling "
                            "the image. Run in cron weekly.",
                            action="store_true")
    args = arg_parser.parse_args()

    log_level = logging.WARN
    config = None

    if args.config_help:
        print("""Rectangled JSON config file keys:
"username" - your github username,
"email" - the email associated with your github account,
"password" - your github password,
"image" - the 52x7 image to display,
"repo_name" - the repository's name,
"repo_location" - the directory to place the local repo in,
"repo_file" - name of the file to use for changes in the repo,
"log_file" - file to log output in.""")
        return

    if args.config:
        config = parse_config(args.config)
    else:
        print("Please supply a config.")
        return

    if args.verbose:
        log_level = logging.DEBUG

    if args.init or args.scheduled:  # lol redundant
        rect = Rectangler(config["username"], config["email"],
                          config["password"], config["image"],
                          repo_name=config["repo_name"],
                          repo_location=config["repo_location"],
                          repo_file=config["repo_file"],
                          log=log_level,
                          log_file=config["log_file"])
        rect.start()
