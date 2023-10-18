# diffExcel 文件差异比较工具

该工具用于比较两个Excel文件（前提：两个表字段都相同但是条数不同）的内容差异，并生成一个新的Excel文件，标注差异信息。
## 功能

- 读取两个Excel文件并比较差异。
- 根据比较结果，生成新的Excel文件，标明源文件、目标文件和匹配情况。

# Excel 文件合并工具

该工具用于合并两个Excel文件的特定列，并将合并结果写入新的Excel文件。
## 功能

- 读取两个Excel文件并根据指定列合并数据。
- 将合并后的数据写入新的Excel文件。


## 使用方法

1. **安装依赖包**

确保已安装以下Python库：
   - pandas
     - openpyxl

可通过以下指令安装：
   ```bash
    pip install pandas openpyxl

