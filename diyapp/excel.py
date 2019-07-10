import xlrd
from sqlweb.models import subjecttable


book = xlrd.open_workbook("abc.xlsx")
sheet = book.sheet_by_name("1")

for r in range(1, sheet.nrows):
      subject_a=subjecttable(subjectname=sheet.cell(r,1).value)

      subject_a.subjectname = sheet.cell(r,1).value
      subject_a.subjectshortname          = sheet.cell(r,2).value
      subject_a.contractnunber     = sheet.cell(r,3).value
      subject_a.subjectsum       = sheet.cell(r,4).value
      subject_a.jia = sheet.cell(r,6).value
      subject_a.yi        = sheet.cell(r,5).value
      subject_a.subjectmanager       = sheet.cell(r,15).value
      subject_a.lvhua     = str(sheet.cell(r,8).value)
      subject_a.light        = str(sheet.cell(r,10).value)
      subject_a.yuanjian         = str(sheet.cell(r,9).value)
      subject_a.shuidian          = str(sheet.cell(r,7).value)
      subject_a.begintime   = sheet.cell(r,11).value.replace(".","-")
      subject_a.endtime = sheet.cell(r, 12).value
      subject_a.statment = sheet.cell(r, 13).value
      subject_a.subjectnote = sheet.cell(r, 12).value
      subject_a.percentage = sheet.cell(r, 12).value
      subject_a.save()



