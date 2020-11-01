import argparse
from logging import INFO, DEBUG, basicConfig


def main():
    parser = argparse.ArgumentParser(description="Run a Discord bot")
    parser.add_argument("-t", "--test", help="set for bot to use local variables", action="store_true")
    # log_info = INFO
    log_info = DEBUG # due to these logs on heroku, maybe it's a good idea to set level for now
    args = parser.parse_args()
    if args.test:
        import beta
        beta.setup_env()
        log_info = DEBUG
    basicConfig(level=log_info, style='{', datefmt="%d.%m.%Y %H:%M:%S",
                format="\n{asctime} [{levelname:<8}] {name}:\n{message}")
    from tools import update_subreddits
    update_subreddits()
    from bot import shroomy_bot
    shroomy_bot.run()


if __name__ == '__main__':
    main()
