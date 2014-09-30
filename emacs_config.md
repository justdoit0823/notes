# This is my emacs config mode list #

*  basic common mode

*  python common mode

*  extension mode


# Basic Common Mode #

## 1.1 enable default mode ##

	(require 'ido)
	(ido-mode t)

	;(require 'cua)
	(cua-mode t)
	;在cua-mode开启式，可以用C-c,C-x,C-v来进行区域文本的复制,剪切和粘贴.

	(global-hl-line-mode)
	(global-linum-mode)
	(column-number-mode)
	(column-highlight-mode)
	;开启这四个模式，就可以在buffer里面看到行号，高亮当前行和列，显示当前行和列的数值.

	把上面的代码加到emacs的启动执行文件中就行了。一般地，可以防止在用户自己HOME目录下的.emacs文件中。



## 1.2 install package manager el-get ##

	按装这个比较简单，只需要打开emacs，然后切换到*scratch*这个bufer执行如下lisp代码即可。
	(add-to-list 'load-path "/path/el-get")
	(unless (require 'el-get nil t)
		(url-retrieve
			"https://github.com/dimitri/el-get/raw/master/el-get-install.el"
				(lambda (s)
					(end-of-buffer)
						(eval-print-last-sexp))))
	(el-get 'sync)
	安装完这个之后，就可以通过el-get的一些命令(函数)来添加其他package了。另外，还可以把上面的代码给加到.emacs文件中，同样可以。


## 1.3 install auto-complete ##

	el-get该派上用场了,用M-x键来打开emacs的内部命令执行器输入el-get-install RET auto-complete RET即可。
	(add-to-list 'load-path "/path/auto-complete")
	(require 'auto-complete-config)
	(add-to-list 'ac-dictionary-directories "/path/auto-complete/ac-dict")
	(ac-config-default)
	把上面的lisp代码加到自己的emacs启动文件里面就可以了.


# python common mode #

