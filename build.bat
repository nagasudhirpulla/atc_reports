call activate_env.bat
call pyinstaller index.py --onefile
call xcopy /Y templates\report_template.docx dist\report_template.docx 