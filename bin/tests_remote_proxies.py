import requests
import argparse
import logging
import inspect
from base64 import b64encode  # , b64decode


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
        self.url = "http://www.nicolasechallier.com/"
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/"
        self.user_agent += "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101"
        self.user_agent += " Safari/537.36"
        self.user_agent_header = {"user-agent": self.user_agent}

    def __send_request__(self, url, key, value, headers=None):
        """
        Sends a post request
        Returns the request
        """
        if headers is None:
            r = requests.post(
                url,
                data={key: value})

        else:
            r = requests.post(
                url,
                data={key: value}, headers=headers)
        return r

    def __checkReply__(self, test_name, r, key, value):
        """
        Checks that the reply is OK
        """
        value_tested = key + "=" + str(value)
        test_OK = True
        logging.debug(test_name + "key = {}".format(key))
        logging.debug(test_name + "value = {}".format(value))
        logging.debug(test_name + "reply = {}".format(r.text))
        logging.debug(test_name + "value tested = {}".format(value_tested))

        if r.status_code is not 200:
            logging.info(
                bcolors.WARNING +
                test_name + "did not reply with 200" + bcolors.ENDC)
            test_OK = False

        if r.reason != "OK":
            logging.info(
                bcolors.WARNING +
                test_name + "reason is not \"OK\"" + bcolors.ENDC)
            test_OK = False

        return test_OK

    def postBasic(self):
        """
        Testing that a normal post works
        """
        test_name = "[" + get_name_doc() + "] "
        key = "coucou"
        value = 12524
        logging.debug(test_name + "sending request")
        r = self.__send_request__(
            self.url, key, value, headers=self.user_agent_header)
        self.__checkReply__(test_name, r, key, value)

    def test_octet_stream(self):
        test_name = "[" + get_name_doc() + "] "
        key = "coucou"
        value = 12524
        headers = self.user_agent_header
        headers["Content-Type"] = 'application/octet-stream'
        logging.debug(test_name + "header = {}".format(headers))
        r = self.__send_request__(
            self.url, key, value, headers=headers)
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
            try:
                if i % 50 is 0:
                    logging.info(
                        test_name + "sent {} requests to the server".format(i))
                r = self.__send_request__(
                    self.url,  key, value)
                self.__checkReply__(test_name, r, key, value)
            except requests.exceptions.ConnectionError:
                logging.info(
                    bcolors.WARNING +
                    test_name +
                    "nous avons été viré car trop de connections" +
                    bcolors.ENDC)
                break


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
        logging.info("running method " + m)
        callMethod(user_class, m)


if __name__ == "__main__":
    # get names of methods
    methods = getUserMethodsFromClass(tests)

    # manage arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action="store_true",
                        help='Toogle verbose mode')
    parser.add_argument('--methods', '-m', default="all", type=str, nargs='*',
                        help='The list of tests. ' +
                        'Available are {}. [default: all]'.format(
                            methods + ['all', 'none']))
    args = parser.parse_args()

    # if we don't want to use all the methods
    if args.methods != "all":
        methods = args.methods

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    else:
        logging.basicConfig(level=logging.INFO)

    # stops logging info at each request
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.CRITICAL)

    requests_logger = logging.getLogger('requests.packages.urllib3')
    requests_logger.setLevel(logging.CRITICAL)

    tests = tests()
    runUserMethods(tests, methods)
