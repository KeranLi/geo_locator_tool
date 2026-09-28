# 在有网络的 Windows 机器上运行此脚本生成 dist\geo_locator.exe
python -m pip install pyinstaller requests
python -m PyInstaller --noconfirm --clean --onefile --windowed --name geo_locator geo_locator_ui.py
Write-Host "生成完成：dist\geo_locator.exe"
