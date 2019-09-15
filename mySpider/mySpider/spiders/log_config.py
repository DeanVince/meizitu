# coding=utf8
import logging

logging.basicConfig(level=logging.INFO,
                        filename="{}_log.txt".format(__file__[:-3]),
                        filemode='a',
                        format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)

def main():
    logger.info("this is the first log")
    logger.info("this is the second log")


if __name__ == '__main__':
    main()

