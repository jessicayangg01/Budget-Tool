import os

dataFiles = {}


def load_dataFiles():
    # path = os.path.join("assets", "images")
    for file in os.listdir("assets"):
        dataFiles[file.split(".")[0]] = os.path.join("assets", file)


def get_dataFile(name):
    return dataFiles[name]
