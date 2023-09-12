import sys

import requests


def main():
    response = requests.get("https://www.google.com/")

    if response.ok:
        print("Hello, world!")
        sys.exit(0)
    else:
        print("Something went wrong :(")
        sys.exit(1)


if __name__ == "__main__":
    main()
