
from wcpy.wc_extractor_processor import WCExtractorProcessor, DIRECTION
from wcpy.wc_extractor import WCExtractor, PathNotValidException

import glob, os

VALID_COLUMNS = ["word", "word_count", "files", "file_count", "sentences", "sentence_count"]
VALID_COLUMNS_SET = set(VALID_COLUMNS)


class WCCore:
    """
    The extractor class is the highest level interface and orchestrates the
    file extractors as well as the processors. It handles everything related
    to managing the folder glob expansion and processing/ printing the output.

    Note:
        The file_extension is still a feature that has not been tested with other types of files

    Args:
        limit (int): Limits the number of rows in the output table
        direction (int): Sort direction for elements in table
        filter_words (list): If present, only those words will be shown in output
        output_file (str): If present, output will be saved to file instead of printed to standard output
        file_extension (str): File type to process - everything else will be ignored
        extractor_processor (WCExtractorProcessor): Dependency Injection for WCExtractorProcessor class for testing
        extractor_file (WCExtractor): Dependency injection for WCExtractor class for testing
    """

    def __init__(self, limit=None, direction=DIRECTION.ASCENDING,
                    extractor_file=WCExtractor, filter_words=[],
                    extractor_processor=WCExtractorProcessor,
                    file_extension="txt", output_file=None):

        if output_file and os.path.exists(output_file):
            raise PathNotValidException("A file already exists, please choose a different one: " + output_file)

        # TODO: Check for valid file extension
        self._file_extension = file_extension
        self._limit = limit
        self._direction = direction
        self._extractor_processor = extractor_processor
        self._extractor_file = extractor_file
        self._filter_words = filter_words
        self._output_file = output_file


    def generate_wc_dict(self, paths):
        """
            Generate a dictionary of WC with the words as keys and their Docs, counts and sentences as values

            Args:
                paths (list): The paths to traverse and extract files from

            Returns:
                result_dict: Dictionary containing the WC objects
        """

        result_dict = {}

        self._check_all_root_paths_valid(paths)
        all_file_paths = self._extract_all_paths(paths)

        for path in all_file_paths:
            extractor_file = self._extractor_file(filter_words=self._filter_words)
            extractor_file.extract_wc_from_file(path, result_dict)

        return result_dict


    def generate_wc_list(self, paths):
        """
            Generates a soted list of WC objects from the files in the paths given

            Args:
                paths (list): List of strings with the paths to traverse and find files to extract

            Returns:
                result_list: A list with the sorted WC objects
        """

        dict_wc = self.generate_wc_dict(paths)

        extractor_processor = self._extractor_processor(limit=self._limit, direction=self._direction)
        result_list = extractor_processor.process_dict_wc_to_list(dict_wc)

        return result_list


    def display_wc_table(self, paths, char_limit=50, columns=None):
        """
            Displays the Word Occurences found in the paths given
            it specifies whether it should be printed to the console or
            saved into a file

            Args:
                paths (list): Paths to traverse and find files to execute
                char_limit (int): Number of chars where string cells will be truncated
                columns (list): Columns that will be displayed
        """

        list_wc = self.generate_wc_list(paths)
        headers, rows = self._generate_table(list_wc, char_limit=char_limit, columns=columns)

        # Change the output stream depending on whether we are requiested
        #   to save to a file or not
        #   Provide an anonimous function with print(,end='') to avoid new
        #   lines being printed and enable compatibility with the out_stream func
        out_stream = lambda x: print(x, end='')
        file = None
        if self._output_file:
            file = open(self._output_file, 'w')
            out_stream = file.write

        self._print_table_ascii(headers, rows, out_stream)

        if file: file.close()

    def _check_all_root_paths_valid(self, paths):
        """
            Checks that all the paths in the array given are valid paths

            Args:
                paths (list): List of strings containing all paths to be checked

            Raises:
                PathNotValidException: If a path is not valid, it raises this exception
        """
        for path in paths:
            if not os.path.exists(path):
                raise PathNotValidException(path)

            # TODO: Add support for globbed files
            if "*" in path:
                raise PathNotValidException("Globbed paths (*) are not supported, please just select the folder: " + str(path))


    def _extract_all_paths(self, paths):
        """
            Traverses all folders and subfolders recurisvely, and expands the paths
                the paths must be valid, and can be checked with the
                _check_all_root_paths_valid funciton. If they don't exist it will be
                skipped.

            Args:
                paths: the paths to extract the subpaths from

            Returns:
                all_file_paths: All of the paths and subpaths found
        """
        all_file_paths = []
        for path in paths:
            if not os.path.exists(path):
                continue


            abs_path = os.path.abspath(path)

            if os.path.isdir(abs_path):
                sub_paths = self._expand_folder_paths(abs_path)
                all_file_paths.extend(sub_paths)
            else:
                all_file_paths.append(abs_path)


        return all_file_paths


    def _expand_folder_paths(self, folder_path):
        """
        Recursively finds all the sub-folders from the path given in the parameter

        Args:
            folder_path (string): Path given to find all subfiles and subfolders

        Returns:
            all_sub_paths: List of string containing all sub-paths
        """
        all_sub_paths = []

        if not os.path.exists(folder_path):
            return all_sub_paths

        glob_extension = "**/*." + self._file_extension
        glob_path = os.path.join(folder_path, glob_extension)

        for sub_path in glob.iglob(glob_path, recursive=True):
            all_sub_paths.append(sub_path)

        return all_sub_paths


    def _generate_table(self, list_wc, char_limit=50, columns=None):
        """
        Converts a sorted list of word occurence objects into a row-based
        table containing all the elements of the list in a set of columns.

        Args:
            list (list_wc): A list containing WC objects
            char_limit (int): The maximum number of chars for words to be truncated
            columns (list): A string list containing the columns to show

        Returns:
            headers: A 1-dimensional list of strings containing headers
            rows: A 2-dimensional array containing all the list wc in table format
        """

        # We first check that the columns are valid
        if columns and len(columns):
            columns = [ col.lower() for col in columns ]
            for col in columns:
                if col not in VALID_COLUMNS_SET:
                    raise InvalidColumnException(col)

        # Creating a printable set of rows
        rows = []
        for obj_word in list_wc:
            word = obj_word["word"]
            wc = str(obj_word["word_count"])
            files = []
            sentences = []

            for file_name in obj_word["files"]:
                files.append(file_name.split("/")[-1])
                file_sentences = obj_word["files"][file_name]

                for sentence in file_sentences:
                    sentences.append(sentence)

            # Format documents and sentences for printing
            str_files = ", ".join(files)
            str_sentences = ", ".join(sentences)

            # Truncate all the inputs to the char_limit
            # TODO: This could be made more efficient by using
            #   'continue' in the loop when char_limit is exceeded
            if char_limit:
                if char_limit < 5:
                    print("WARNING: Minimum char limit must be above 5. Changing to 5.")
                    # We substract 3 to add the '...' truncations
                    char_trunc = char_limit - 3
                str_files = str_files[:char_limit] + "..." if len(str_files) > char_limit else str_files
                str_sentences = str_sentences[:char_limit] + "..." if len(str_sentences) > char_limit else str_sentences

            count_files = str(len(files))
            count_sentences = str(len(sentences))

            # Note: if column becomes longer, it will be necessary
            #   to create a set to improve time complexity
            if columns and len(columns):
                row_cols = []
                if VALID_COLUMNS[0] in columns:
                    row_cols.append(word)
                if VALID_COLUMNS[1] in columns:
                    row_cols.append(wc)
                if VALID_COLUMNS[2] in columns:
                    row_cols.append(str_files)
                if VALID_COLUMNS[3] in columns:
                    row_cols.append(count_files)
                if VALID_COLUMNS[4] in columns:
                    row_cols.append(str_sentences)
                if VALID_COLUMNS[5] in columns:
                    row_cols.append(count_sentences)

                rows.append(row_cols)
            else:
                rows.append([ word, wc, str_files, count_files, str_sentences, count_sentences ])

        # We define the headers
        headers = columns if columns and len(columns) else VALID_COLUMNS

        return headers, rows

    def _print_table_ascii(self, headers, rows, out_stream=print):
        """
        Converts a list of headers and a list of rows in an ASCII table
        """

        # Here, get the max_widths of all the data
        #   To do this, first transpose / group all strings by columns.
        #   Then get the strings with the most number of chars in each columns.
        #   Finally count the number of characters in the longest string.
        #   Those are our max_widths
        max_widths = [ len(max(columns, key=len)) for columns in zip(*rows, headers) ]

        # First we create a row divider
        #   Print a number of dashes relative to the width of each column
        #   by using the * python operator.
        #   The separator of each is also 3 characters long, same as above
        out_stream(' ' + '-+-'.join( '-' * width for width in max_widths ) + '\n')

        # Now print the headers
        #   Using Python's format functionality, as it allows us to specify a
        #   standard width, which will make our table consistent and symmetric
        #   In this case, our width is 'max_width', and we print the title within that
        #   and separate each of the strings by a pipe symbol '|'
        out_stream('|' + ' | '.join( format(title, "%ds" % max_width) for max_width, title in zip(max_widths, headers) ) + '|'+ '\n')

        # Another row divider
        out_stream('|' + '-+-'.join( '-' * width for width in max_widths ) + '\n')

        # Now print all the data
        #   This uses a similar approach as the print map used above
        #   when printing the headers
        for row in rows:
            out_stream('|' + " | ".join( format(cdata, "%ds" % width) for width, cdata in zip(max_widths, row) ) + '|'+ '\n')

        # Final row divider
        out_stream(' ' + '-+-'.join( '-' * width for width in max_widths ) + '\n')


class InvalidColumnException(Exception):
    """
    Thrown when a column provided is not valid from the set of columns provided
    """
    def __init__(self, col):
        Exception.__init__(self, "Column provided is not valid: " + str(col) + ". Valid columns are: " + str(VALID_COLUMNS))

