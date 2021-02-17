


@echo OFF
set /p FolderToSearch="Folder To Search: "
set /p ext="Extension to Find: "
set /p backuplocation="Clean Backup Save Location: "
call "C:\Users\Justin Jaro\Anaconda3\Scripts\activate.bat" opencv-env

@REM python %~dp0\burninimagename.py "M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\scripts\python\image\Testing\HDR - Original" png "M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\scripts\python\image\Testing\temp"
python %~dp0\burninimagename.py "%FolderToSearch%" %ext% "%backuplocation%"


call conda deactivate



pause