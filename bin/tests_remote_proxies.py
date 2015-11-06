import requests
import argparse
import logging
import inspect
from base64 import b64encode, b64decode


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    def __send_request__(self, url, key, value):
        """
        Sends a post request
        Returns the request
        """
        r = requests.post(
            url,
            data={key: value})
        return r

    def __checkReply__(self, test_name, r, key, value):
        """
        Checks that the reply is OK
        """
        test_name = "[" + get_name_doc() + "] "
        value_tested = key + "=" + str(value)
        logging.debug(test_name + "key = {}".format(key))
        logging.debug(test_name + "value = {}".format(value))
        logging.debug(test_name + "reply = {}".format(r.text))
        logging.debug(test_name + "value tested = {}".format(value_tested))

        if r.status_code is not 200:
            logging.info(
                bcolors.WARNING +
                test_name + "did not reply with 200" + bcolors.ENDC)

        if r.reason != "OK":
            logging.info(
                bcolors.WARNING +
                test_name + "reason is not \"OK\"" + bcolors.ENDC)

        if r.text != value_tested:
            logging.info(
                bcolors.WARNING +
                test_name + "text replied is not ok" + bcolors.ENDC)

    def postBasic(self):
        """
        Testing that a normal post works
        """
        key = "coucou"
        value = 12524
        r = self.__send_request__(self.url, key, value)
        test_name = "[" + get_name_doc() + "] "
        self.__checkReply__(test_name, r, key, value)

    def postB64(self):
        """
        Test proxy accepts b64 type requests
        """
        key = "coucou"
        value = b64encode(b"salut")

        test_name = "[" + get_name_doc() + "] "
        r = self.__send_request__(self.url, key, value)

        logging.debug(test_name + "key = {}".format(key))
        logging.debug(test_name + "value = {}".format(value))
        logging.debug(test_name + "reply = {}".format(r.text))
        self.__checkReply__(test_name, r, key, value.decode())

    def requestOverload(self):
        """
        Tests that a proxy does not stop a high level of requests per seconds
        """
        test_name = "[" + get_name_doc() + "] "
        number_of_requests = 1000
        key = "coucou"
        value = 1
        for i in range(0, number_of_requests):
            if i % 20 is 0:
                logging.info(
                    test_name + "sent {} requests to the server".format(i))
            r = self.__send_request__(self.url, key, value)
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

    # stops logging info at each request
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.CRITICAL)

    methods = getUserMethodsFromClass(tests)
    tests = tests()
    runUserMethods(tests, methods)