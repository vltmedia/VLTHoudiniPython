


@REM @echo OFF
echo 1 : %1 
echo 2 : %2 
echo 3 : %3

call "C:\Users\Justin Jaro\Anaconda3\Scripts\activate.bat" opencv-env

@REM python %~dp0\burninimagename.py "M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\scripts\python\image\Testing\HDR - Original" png "M:\Projects\Sketches\ScifiSketches\01-Working\28-JJ\04-3D\Scifi-Kitbash\ScifiKitbash\scripts\python\image\Testing\temp"
python %~dp0\burninimagename.py %1 %2 %3


call conda deactivate



