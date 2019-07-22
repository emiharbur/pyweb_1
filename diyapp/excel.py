import xlrd



book = xlrd.open_workbook("abc.xlsx")
sheet = book.sheet_by_name("1")

for r in range(1, sheet.nrows):

      subject_a_subjectname = sheet.cell(r,1).value
      subject_a_subjectshortname          = sheet.cell(r,2).value
      subject_a_contractnunber     = sheet.cell(r,3).value
      subject_a_subjectsum       = sheet.cell(r,4).value
      subject_a_jia = sheet.cell(r,6).value
      subject_a_yi        = sheet.cell(r,5).value
      subject_a_subjectmanager       = sheet.cell(r,15).value
      subject_a_lvhua     = str(sheet.cell(r,8).value)
      subject_a_light        = str(sheet.cell(r,10).value)
      subject_a_yuanjian         = str(sheet.cell(r,9).value)
      subject_a_shuidian          = str(sheet.cell(r,7).value)
      subject_a_begintime   = str(sheet.cell(r,11).value).replace(".","-")
      subject_a_endtime = sheet.cell(r, 12).value
      subject_a_statment = sheet.cell(r, 13).value
      subject_a_subjectnote = sheet.cell(r, 12).value
      subject_a_percentage = sheet.cell(r, 12).value


