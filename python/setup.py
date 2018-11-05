"""
Downloads dependencies
"""

import urllib

def getSys64():
    """
    Downloads MiTeC System Information X
    """

    link = "http://mitec.cz/Downloads/MSIX64.ZIP"

    archive = urllib.URLopener()
    archive.retrieve(url=link, filename="MSIX64.ZIP")

if __name__ == "__main__":
    #getSys64()
    print __file__