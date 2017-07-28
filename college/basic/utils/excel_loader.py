#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openpyxl import load_workbook


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
