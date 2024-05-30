# Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
# Use of this file is governed by the BSD 3-clause license that
# can be found in the LICENSE.txt file in the project root.
#

from io import StringIO


def str_collection(val, begin, end):
    with StringIO() as buf:
        buf.write(begin)
        first = True
        for item in val:
            if not first:
                buf.write(", ")
            buf.write(unicode(item))
            first = False
        buf.write(end)
        return buf.getvalue()


def str_list(val):
    return str_collection(val, "[", "]")


def str_set(val):
    return str_collection(val, "{", "}")


def escapeWhitespace(s, escapeSpaces):
    with StringIO() as buf:
        for c in s:
            if c == " " and escapeSpaces:
                buf.write("\u00B7")
            elif c == "\t":
                buf.write("\\t")
            elif c == "\n":
                buf.write("\\n")
            elif c == "\r":
                buf.write("\\r")
            else:
                buf.write(unicode(c))
        return buf.getvalue()
