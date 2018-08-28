北航教务一键评教
=======

北航有个奇怪要求，不评教不能查看成绩。但是，这么多教师，每个教师还有好多个选项，全部评价完需要10来分钟。
故写一段python脚本，完成该功能。

**安装依赖及运行**

以windows10 PowerShell为例：

```
# 1. 安装Requests
pip install requests（可能需要管理员权限）
# 2. 安装BeautifulSoup4
pip install beautifulsoup4 (可能需要管理员权限）
# 3. 运行
python main.py
```

**功能简介**

1. 自动选择最佳评价（由于至少需要有一个选项与其他不同，故第一项选择为良，其他全部选择优秀）

2. 统一认证自动登陆（提供学号、密码，一键傻瓜式操作）


**其他问题**

由于本脚本仅在本机测试（windows 10）通过，无法保证其他环境下能正常使用。如有任何问题，欢迎issue中交流。
