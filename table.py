from typing import List

_align = {
    'l': '<',
    'r': '>',
    'c': '^'
}


class Table:
    """ A simple table class for printing data in tabular format.

    +---------------------------------+
    |             Title               |
    +---------------------------------+
    | Header1      Header2     ...    |
    |=================================|
    | Cell(1,1)    Cell(1,2)   ...    |
    | Cell(2,1)    Cell(2,2)   ...    |
    | ...           ...        ...    |
    +---------------------------------+

    Attributes:
        title (str): Title of the table.
        headers (List[str]): Column headers.
        rows (List[List[Any]]): Table rows.
        align (str): Alignment of each column. 'l' for left, 'r' for right, 'c' for center. Default: 'l' * len(headers)
        col_spacing (int): Spacing between columns.
        margin (int): Margin between table and left/right border.
        unit (List[str]): Unit of each column. Default: [''] * len(headers)

    .. note::
        Multi-line cells are not supported.
    """

    def __init__(self, title: str, headers: List[str], align: str = '',
                 col_spacing: int = 5, margin: int = 1, unit: List[str] = None):
        self.title = title
        self.headers = headers
        self.rows = []
        self.align = (align or 'l' * len(headers)).lower()
        self.col_spacing = col_spacing
        self.margin = margin
        self.unit = unit or [''] * len(headers)
        assert set(self.align) <= {'l', 'r', 'c'}
        assert len(self.align) == len(self.headers)
        assert len(self.unit) == len(self.headers)

    def add_row(self, row: List[str]):
        assert len(row) == len(self.headers)
        self.rows.append(row)

    def print(self):
        print(str(self))

    def __str__(self):
        col_sp = ' ' * self.col_spacing
        max_widths = [len(h) for h in self.headers]
        aligns = [_align[a] for a in self.align]
        for row in self.rows:
            for i, cell in enumerate(row):
                max_widths[i] = max(max_widths[i], len(str(cell) + self.unit[i]))

        full_width = sum(max_widths) + self.col_spacing * (len(self.headers) - 1)
        assert len(self.title) <= full_width, f'title is too long: {self.title}'

        lb = '|' + ' ' * self.margin  # left border
        rb = ' ' * self.margin + '|'  # right border
        tbb = '+' + '-' * (full_width + 2 * self.margin) + '+'  # top and bottom border
        sep = '|' + '=' * (full_width + 2 * self.margin) + '|'  # separator between header and table

        rows = []
        for row in [self.headers] + self.rows:
            header = row is self.headers  # do not add unit to header
            rows.append(
                lb + col_sp.join(f'{str(cell) + ("" if header else unit):{align}{width}}'
                                 for cell, width, align, unit in zip(row, max_widths, aligns, self.unit)) + rb)

        title = lb + self.title.center(full_width) + rb

        return '\n'.join([tbb, title, tbb, rows[0], sep] + rows[1:] + [tbb])

    def __repr__(self):
        return f'<Table {self.title}>'


__all__ = ['Table']
