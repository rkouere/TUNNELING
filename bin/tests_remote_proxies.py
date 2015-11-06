import requests
import argparse
import logging
import inspect
from base64 import b64encode, b64decode


def get_name_doc():
    """
    Returns the name of the current method
    """
    outerframe = inspect.currentframe().f_back
    name = outerframe.f_code.co_name
    return name


class tests:
    def __init__(self):
        self.url = "http://nicolasechallier.com/proxy/home.php"

    def postBasic(self):
        """
        Testing that a normal post works
        """
        key = "coucou"
        value = 12524
        r = requests.post(
            self.url,
            data={key: value})
        test_name = "[" + get_name_doc() + "] "
        self.__checkReply__(test_name, r, key, value)

    def __checkReply__(self, test_name, r, key, message):
        """
        Checks that the reply is OK
        """
        if r.status_code is not 200:
            logging.info(test_name + "did not reply with 200")

        if r.reason != "OK":
            logging.info(test_name, "reason is not \"OK\"")

        if r.text != 'coucou=12524':
            logging.info(test_name + "text replied is not ok")

    def postB64(self):
        """
        Test proxy accepts b64 type requests
        """
        key = "coucou"
        value = b64encode(b"salut")

        test_name = "[" + get_name_doc() + "] "
        r = requests.post(
            self.url,
            data={key: value})
        self.__checkReply__(test_name, r, key, value)


def getUserMethodsFromClass(c):
    """
    Lists user's defined methods
    """
    methods = dir(c)
    user_methods = []
    for i in methods:
        if not i.startswith("__"):
            user_methods.append(i)
    return user_methods


def callMethod(o, name):
    getattr(o, name)()


def runUserMethods(user_class, methods):
    for m in methods:
        callMethod(user_class, m)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Toogle verbose mode')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    else:
        logging.basicConfig(level=logging.INFO)

    methods = getUserMethodsFromClass(tests)
    tests = tests()
    runUserMethods(tests, methods)
