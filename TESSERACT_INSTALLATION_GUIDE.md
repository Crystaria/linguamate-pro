# Tesseract OCR 安装指南

## 概述
Tesseract OCR 是一个开源的光学字符识别引擎，用于从图片中提取文字内容。本指南将帮助您在Windows系统上安装和配置Tesseract OCR。

## Windows 安装方法

### 方法一：使用预编译二进制文件（推荐）

1. **下载Tesseract**
   - 访问官方下载页面：https://github.com/UB-Mannheim/tesseract/wiki
   - 下载最新版本的Windows安装包（.exe文件）
   - 推荐下载：`tesseract-ocr-w64-setup-5.x.x.exe`

2. **安装Tesseract**
   - 运行下载的安装程序
   - 选择安装路径（建议使用默认路径：`C:\Program Files\Tesseract-OCR\`）
   - 在安装过程中，确保选择以下语言包：
     - English (eng)
     - Chinese Simplified (chi_sim)
     - Chinese Traditional (chi_tra)

3. **配置环境变量**
   - 打开"系统属性" → "高级" → "环境变量"
   - 在"系统变量"中找到"Path"，点击"编辑"
   - 添加Tesseract安装路径：`C:\Program Files\Tesseract-OCR\`
   - 点击"确定"保存

4. **验证安装**
   ```cmd
   tesseract --version
   ```
   如果显示版本信息，说明安装成功。

### 方法二：使用包管理器

#### 使用 Chocolatey
```powershell
# 安装Chocolatey（如果未安装）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装Tesseract
choco install tesseract
```

#### 使用 Scoop
```powershell
# 安装Scoop（如果未安装）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# 安装Tesseract
scoop install tesseract
```

## 语言包安装

### 下载语言包
1. 访问：https://github.com/tesseract-ocr/tessdata
2. 下载以下语言包文件：
   - `eng.traineddata` (英文)
   - `chi_sim.traineddata` (简体中文)
   - `chi_tra.traineddata` (繁体中文)

### 安装语言包
1. 将下载的`.traineddata`文件复制到Tesseract安装目录的`tessdata`文件夹中
2. 默认路径：`C:\Program Files\Tesseract-OCR\tessdata\`

## 验证安装

### 命令行测试
```cmd
# 测试英文识别
tesseract --list-langs

# 测试图片识别（需要准备一张包含文字的图片）
tesseract image.png output.txt -l eng

# 测试中英文混合识别
tesseract image.png output.txt -l eng+chi_sim
```

### Python测试
```python
import pytesseract
from PIL import Image

# 测试Tesseract是否可用
try:
    print(pytesseract.get_tesseract_version())
    print("Tesseract安装成功！")
except Exception as e
    print(f"Tesseract未正确安装：{e}")
```

## 常见问题解决

### 问题1：'tesseract' 不是内部或外部命令
**解决方案**：
- 检查环境变量PATH是否包含Tesseract安装路径
- 重启命令行或IDE
- 重新安装Tesseract

### 问题2：语言包未找到
**解决方案**：
- 确认语言包文件已正确放置在`tessdata`文件夹中
- 检查文件名是否正确（如`eng.traineddata`）
- 使用`tesseract --list-langs`查看可用语言

### 问题3：Python中pytesseract报错
**解决方案**：
```python
# 如果pytesseract找不到tesseract，可以手动指定路径
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 项目集成

安装完成后，您的LinguaMate AI项目将自动使用真实的OCR功能：

1. **重启后端服务器**
   ```cmd
   python backend\main_local.py
   ```

2. **测试图片上传功能**
   - 上传包含文字的图片
   - 系统将自动使用Tesseract进行OCR识别
   - 提取真实的文字内容进行分析

## 性能优化建议

1. **图片预处理**
   - 确保图片清晰度足够
   - 文字与背景对比度明显
   - 避免倾斜或扭曲的文字

2. **语言选择**
   - 根据图片内容选择正确的语言参数
   - 中英文混合内容使用`eng+chi_sim`
   - 纯英文内容使用`eng`

3. **批量处理**
   - 对于大量图片，考虑使用多线程处理
   - 可以预先调整图片大小以提高处理速度

## 技术支持

如果遇到安装问题，可以：
1. 查看Tesseract官方文档：https://tesseract-ocr.github.io/
2. 检查GitHub Issues：https://github.com/tesseract-ocr/tesseract/issues
3. 参考社区论坛和Stack Overflow

---

安装完成后，您的LinguaMate AI将具备完整的OCR功能，能够从图片中准确提取文字内容进行语言分析！

