call activate_env.bat
call pyinstaller index.py --onefile --distpath ./atc_reports_dist
call xcopy /Y templates\report_template.docx atc_reports_dist\report_template.docx 