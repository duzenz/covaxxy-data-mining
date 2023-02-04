import json

import xlsxwriter
import os

DOWNLOADS_FOLDER = "downloads/"
PROGRESS_FOLDER = "reporting"

with open('dataset/iffy.txt', encoding="utf8") as f:
    lines = [line.rstrip() for line in f]

for (root, dirs, file) in os.walk(DOWNLOADS_FOLDER):
    for directory in dirs:
        for (rootSub, dirsSub, fileSub) in os.walk(DOWNLOADS_FOLDER + directory):
            workbook = xlsxwriter.Workbook(PROGRESS_FOLDER + "/" + directory + ".xlsx")
            worksheet = workbook.add_worksheet()
            row = 0
            col = 0
            for filename in fileSub:
                f = open(DOWNLOADS_FOLDER + directory + "/" + filename, encoding="utf8")
                data = json.load(f)
                for tweet in data["data"]:
                    worksheet.write(row, col, tweet["id"])
                    worksheet.write(row, col + 1, tweet["text"])
                    res = [ele for ele in lines if (ele in tweet["text"])]
                    if bool(res):
                        worksheet.write(row, col + 2, 0)
                    else:
                        worksheet.write(row, col + 2, 1)
                    row += 1
            workbook.close()
print("finished")
