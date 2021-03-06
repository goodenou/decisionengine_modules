import time
import logging

"""
Load python object
"""


def load(python_file, retries=0, timeout=0):
    """
    Load constants from file.

    :type constants_file: :obj:`file`
    :arg constants_file: configuration file as python dict

    :rtype: :obj:`object`

    """

    code = None
    config = None
    retries = max(1, retries)
    timeout = max(1, timeout)
    for i in range(retries):
        try:
            with open(python_file, "r") as f:
                code = "config=" + "".join(f.readlines())
            if code:
                exec(code)
            break
        except IOError:
            logging.getLogger.warning(f"config load failed in de_modules, {retries-i} retries")
            time.sleep(timeout)
    else:
        logging.getLogger().exception(f"cannot load {python_file}")
        raise RuntimeError()

    return config


if __name__ == '__main__':
    config = load('spot_price_config_sample.py')
    print(config)
