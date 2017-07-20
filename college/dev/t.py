from openpyxl import load_workbook
wb = load_workbook(filename='学校标识码（整合）.xlsx', read_only=True)
ws = wb.active
r = ws.rows
first_row = next(r)
l = [cell.value for cell in first_row]
print(l)
l = []
for row in r:
    temp = []
    for cell in row:
        temp.append(str(cell.value))
    l.append(temp)
print(l)