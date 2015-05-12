Effective Python
================
	整体感觉不错，章节比较系统，包括了比较完整的python web开发栈。部分细节存在一些待提高的地方，
	如少许错别字，少数术语表述欠妥(个人认为)，以及比较坑爹的代码排版(硬伤).



对部分条目的一些看法
====================
* 建议10中的Lazy evaluation
  在python3中，如range, map, filter等其实都被实现成了Lazy的。只补充一句，Lazy的虽好，
  但如果需要迭代多次的话，这些都会出问题。因为这些只能迭代一次，如果想再次迭代就没有数据，
  而且比较隐蔽。

* 建议31中的传值还是传引用
  在python中应该不用去纠结是值还是引用，只需要确认一点，名称绑定和命名空间，传参时只不过是将参数名与参数对象进行了绑定.
  具体可以查看python官方文档
[Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)。

* 建议66中的生成器
  在python中生成器函数和生成器对象是有区分的，我觉得得强调这种区别。通过inspect模块中的isgenerator和isgeneratorfunc可以很明白地了解。
  另外，生成器对象只是实现了迭代器的协议，而本身并不是迭代器。

* 建议61中的实现只读属性
  例子当中的代码有少数问题，实现只读属性的思路是对的，通过在类中添加与对象的属性名相同的非数据描述符.
通过控制属性的读写来实现，具体的属性顺序可以看python官方文档
[attribute access](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)
