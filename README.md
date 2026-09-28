# 自然语言经纬度查询工具 | Natural-language Geocoder

**开发者 / Developer: Keran Li**

## 功能 | Features

- 中文和 English 双语图形界面 / Bilingual Chinese-English GUI
- 使用自然语言地点查询经度和纬度 / Geocode natural-language place names
- 显示匹配地址、数据源和坐标系 / Show address, provider and CRS
- 一键复制坐标 / Copy coordinates with one click
- 支持高德 Web 服务 API 和 OpenStreetMap Nominatim / Supports AMap Web Service API and OpenStreetMap Nominatim

## 直接运行 EXE | Run the EXE

双击 `dist\\geo_locator.exe`，无需安装 Python。

Double-click `dist\\geo_locator.exe`; Python is not required.

## 开发运行 | Run from source

```powershell
python -m pip install requests
python geo_locator_ui.py
```

## 高德 Key | AMap key

请使用高德“Web服务 API”类型 Key，并开通地理编码 API。不要使用 JavaScript API Key。

Use an AMap **Web Service API** key with the Geocoding API enabled. A JavaScript API key does not work with this desktop application.

在 GUI 的“高德 Web Key”输入框中填写即可。

Paste it into the “AMap Web Key” field in the GUI.

## 打包 EXE | Build the EXE

在可联网的 Windows CMD 中运行：

Run the following in a network-enabled Windows CMD:

```cmd
build_exe.bat
```

或使用 PowerShell：

Or use PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\\build_exe.ps1
```

输出文件 / Output: `dist\\geo_locator.exe`
