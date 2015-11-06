import requests
import argparse
import logging
import inspect


def get_name_doc():
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
        r = requests.post(
            self.url,
            data={"coucou": 12524})
        test_name = "[" + get_name_doc() + "] "
        if r.status_code is not 200:
            logging.info(test_name + "did not reply with 200")

        if r.reason != "OK":
            logging.info(test_name, "reason is not \"OK\"")

        if r.text != 'coucou=12524':
            logging.info(test_name + "text replied is not ok")


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
