"""
Top Service

This service interfaces with the linux 'sensors' command.

"""
import os

class TopService():

    def get_top_data(self):
        """
        Call 'sensors', pull out the cpu, mb, and vid temps.
        Return these as separate values, along with the whole dump of the command.
        """

        top_handle = os.popen('top -n 1 -b')
        top_by_line = []

        first_line = ""
        header_by_line = []
        column_names = []
        rows = []

        is_first = True
        is_header = False
        is_column_names = False
        for line in top_handle.readlines():

            top_by_line.append(line)

            if is_header:
                if line == "\n":
                    is_header = False
                    is_column_names = True
                else:
                    header_by_line.append(line)

            elif is_first:
                first_line = line
                is_first = False
                is_header = True

            elif is_column_names:
                column_names = line.split()
                is_column_names = False

            # Else where dealing with the tabular data
            else:
                row = line.split()
                index = len(rows)
                rows.append([])
                for column in row:
                    rows[index].append(column)



        get_top_data_result = {
            'first_line': first_line,
            'header_by_line': header_by_line,
            'column_names': column_names,
            'rows': rows
        }

        return get_top_data_result
