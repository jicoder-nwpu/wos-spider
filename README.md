# 使用说明

### 安装包

```bash
pip install -r requirements.txt
```

### 将需要查询论文的相关信息填入tasks中

```python
tasks = [
    {
        "url": "被引检索页面",
        "o_authors": "原文作者列表",
        "o_title": "原文题目"
    },
    {
        "url": "被引检索页面",
        "o_authors": "原文作者列表",
        "o_title": "原文题目"
    }
]

download_path = r'存储中间文件的目录'
```

### 运行程序

```bash
python spider.py
```

