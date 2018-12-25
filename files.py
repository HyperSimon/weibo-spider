# coding=utf-8

def save(filename, contents):
    fh = open(filename, 'w+')
    fh.write(contents)
    fh.close()


def read(filename):
    fh = open(filename, "r")
    content = fh.readline()
    return content
