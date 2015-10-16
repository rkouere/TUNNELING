#! /usr/bin/env python3

hardReturn = "\r\n"


class httpPacket:
    def __init__(self):
        """
        Set the typical header
        """
        self.header = (
            "HTTP/1.1 200 OK" + hardReturn
            + "Content-type: application/octet-stream" + hardReturn
            + "Transfer-Encoding: chunked" + hardReturn)
        self.data = ""
        self.contentLength = ""

    def setCookie(self, token):
        """
        Sets a cookie. Has to be a digit
        """
        self.header += "Set-Cookie: tok=" + str(token) + hardReturn

    def setData(self, data):
        """
        Sets the data to send
        Sets the length of the data
        """
        self.data = data
        self.setContentLength()

    def setContentLength(self):
        self.contentLength = 
            "Content-length: " + str(len(self.data)) + hardReturn

    def getPacket(self):
        """
        Constructs the http packet to send
        """
        packet = self.header + hardReturn + self.contentLength + self.data
        return packet


def test():
    print("test")


def main():
    packet = httpPacket()
    packet.setCookie(1234)
    packet.setData("salut tout le monde")
    print(packet.getPacket())

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
