
Octave
======

	Octave是一个与Matlab语法兼容的开放源代码科学计算及数值分析工具。


Octave运算介绍
--------------


* 矩阵相乘

		C = A * B

		若A, B皆为矩阵, 则A的列数必须等于B的行数。


* 矩阵相除

		C = A / B

		若A, B皆为矩阵，则A的列数必须大于等于B的列数。




* 矩阵加减

		C = A + B

		若A, B皆为矩阵, 则必须有相同的阶数。


* element-by-element运算

		C = A .operator B

		A, B矩阵中相对应的元素进行运算，有阶数要求。


* 转置矩阵

		A'

		表示A的转置矩阵。


* 单位矩阵

		eye

		返回N阶单位矩阵


* 魔法矩阵

		magic

		返回3阶以上的魔法矩阵，实际则是N阶数独的解。


代码编写
--------

* 物理结构

		存在模块划分，函数，表达式，逻辑分支等。

* 语法

		与matlab兼容，没有过多约束。

* 执行

		存在REPL交互环境，上手尝试代价小。

* 编写

		代码纯文本，自选编辑器。


工具
----

* GNU Octave

		GUI版本，集编辑调试与一体，不过Ubuntu上面的gedit编辑卡得要死。

* octave-cli

		命令行版本，推荐使用。Mac上面可以直接brew安装，配置plot显示终端费点劲。



引用
----

* <http://www.gnu.org/software/octave/doc/v4.0.1/Arithmetic-Ops.html>
