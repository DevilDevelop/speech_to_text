winget install --id Microsoft.VCRedist.2015+.x64 -e
winget install ffmpeg
python -m venv venv
./venv/Scripts/Activate.ps1
pip install -r requirements_windows.txt