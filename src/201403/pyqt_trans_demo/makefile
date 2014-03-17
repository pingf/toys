#-*- coding:utf-8 -*-

ok: run

# 下面就是翻译的过程:
# 首先提取出代码里面需要翻译的部分
update:
	pylupdate4 main.py -ts plabel_zh_CN.ts

# 然后用linguist这个工具把东西翻译完
trans:
	linguist-qt4 plabel_zh_CN.ts

# 最后编译代码:
build-ts:
	lrelease-qt4 plabel_zh_CN.ts

# 好的, 可以执行了:
run:
	python main.py