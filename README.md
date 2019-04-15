## 快乐背单词

### 环境相关

主要配置

**python 主要配置**
```shell
Package              Version
-------------------- --------
Django               2.0.13
django-bootstrap4    0.0.8
django-reversion     3.0.3
mysqlclient          1.4.2
xadmin               2.0.1
xlrd                 1.2.0
xlwt                 1.3.0
```

**其他配置**

```latex
latex {pdflatex}
mysql 5.6
```

我只是写了个windows版本，写给自己玩玩的

### 操作 相关

在import 页面可以上传CSV 或者 EXCEL 文件。之后点背诵就可以返回latex编译的单词本啦
感觉自己有些代码写的稀烂。但是又不知道咋写是正确的1551

关于 excel 或者 csv 的格式请参考 `xls\`目录下的`template.csv`和`template.xlsx`

### TODO LIST

- [x] django 信号量机制 删除多余的EXCEL 文件
- [x] Latex 文本序号
- [ ] 单词收藏按钮
- [ ] 单词/单词本搜索按钮
- [ ] Latex 答案纸
- [x] 默写单词乱序
- [x] 拖动放入 excel
- [ ] PDF 文件入库

**暂时不考虑加入的内容**

- [ ] 多用户
