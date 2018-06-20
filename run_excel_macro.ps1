$xlApp = New-Object -ComObject "Excel.Application"
$workbook = $xlApp.Workbooks.Open("C:\usr\FinancialAnalysisTool_Portfolio\Financial_Tools\FORMATTING.xlsm")
$workbook.close($false)
$xlApp.quit()