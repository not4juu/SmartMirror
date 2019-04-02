import Logger

"""Creates a singleton instance for program Logger buffer

Parameters
----------
file_loc : str
    The file location of the spreadsheet
print_cols : bool, optional
    A flag used to print the columns to the console (default is False)

Returns
-------
list
    a list of strings representing the header columns
"""

def main():
    Logger.init_logger()
    Logger.logging.info('Run main')


if __name__ == "__main__":
    main()