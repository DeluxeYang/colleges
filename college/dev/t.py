from openpyxl import load_workbook
filename = '学校标识码（整合）.xlsx'


def load_excel(excel_file):
    wb = load_workbook(filename=excel_file, read_only=True)
    return wb


def get_excel_head(wb):
    ws = wb.active
    first_row = next(ws.rows)
    excel_head = [cell.value for cell in first_row]
    return excel_head


def get_excel_body_generator(wb):
    ws = wb.active
    _generator = ws.rows
    next(_generator)  # 去掉head
    for row in _generator:
        temp = []
        for cell in row:
            temp.append(str(cell.value))
        yield temp


def empty_is_false(content):
    """
    有内容
    :param content:
    :return:
    """
    return True if content != "None" else False

wb = load_excel(filename)
g = get_excel_body_generator(wb)
for _g in g:
    print(_g)
    if empty_is_false(_g[9]):
        print(_g[9])
