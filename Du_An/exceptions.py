
#* Exception raises when a dataframe is not clean (has some empty line for example)
class DfNotClean(Exception):
    pass


#* Use when validating columns in a dataframe
class InvalidColumn(Exception):
    pass

class MissingIndex(Exception):
    pass

class MissingInfo(Exception):
    pass