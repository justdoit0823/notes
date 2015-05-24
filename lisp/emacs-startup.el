
;; This is my emacs startup file.

;; Author: SenbinYu


(setq package-list '("fill-column-indicator" "jedi" "markdown-mode"
		     "ace-jump-mode" "multiple-cursors" "undo-tree"
		     "projectile" "git-emacs"))

(defun customize-color ()
  "customize color"
  (add-to-list 'default-frame-alist '(foreground-color . "#DEF"))
  (add-to-list 'default-frame-alist '(background-color . "#555"))
  )


(defun set-default-language ()
  "set default language"
  (set-language-environment "utf-8")
  (setq locale-coding-system 'utf-8)
  (set-buffer-file-coding-system 'utf-8)
  (setenv "LANG" "zh_CN.UTF-8")
  (set-locale-environment "zh_CN.UTF-8")
  )

(defun load-ido ()
  "load ido mode"
  (require 'ido)
  (ido-mode t)
  )


(defun load-undo-tree ()
  "load undo tree"
  (require 'undo-tree)
  (undo-tree-mode t)
  )

(defun load-multiple-cursor ()
  "load multiple cursor"
  (require 'multiple-cursors)
  (global-set-key (kbd "C-S-c C-S-c") 'mc/edit-lines)
  )

(defun load-projectile ()
  "load project mode"
  (require 'projectile)
  (projectile-global-mode)
  (add-hook 'python-mode-hook 'projectile-mode)
  )

(defun set-markdown ()
  "set markdown"
  (custom-set-variables
   ;; custom-set-variables was added by Custom.
   ;; If you edit it by hand, you could mess it up, so be careful.
   ;; Your init file should contain only one such instance.
   ;; If there is more than one, they won't work right.
   '(markdown-coding-system (quote utf-8))
   '(markdown-content-type "text"))
  )

(defun set-frame-title ()
  "set frame title"
  (setq frame-title-format
	(list (format "%s %%S: %%j " (system-name))
	      '(buffer-file-name "%f" (dired-directory dired-directory "%b"))))
  )

(defun load-fill-indicator ()
  "load file column indicator"
  (add-to-list 'load-path "~/.emacs.d/fill_column_indicator")
  (require 'fill-column-indicator)
  (define-globalized-minor-mode
    global-fci-mode fci-mode (lambda () (fci-mode 1)))
  (global-fci-mode t)
  (setq-default fill-column 81)
  )

(defun load-git-emacs ()
  "load git emacs"
  (add-to-list 'load-path "~/.emacs.d/git-emacs")
  (require 'git-emacs)
  )

(defun set-exec-path ()
  "set exec path"
  (setenv "PATH" (concat (getenv "PATH") ":/usr/local/bin"))
  (setq exec-path (append exec-path '("/usr/local/bin")))
  )

(defun load-jedi ()
  "load jedi"
  (add-hook 'python-mode-hook 'jedi:setup)
  )

(defun enable-line-column ()
  "enable line column mode"
  (global-hl-line-mode)
  (global-linum-mode)
  (column-number-mode)
  )

(defun load-el-get ()
  "load el-get"
  (add-to-list 'load-path "~/.emacs.d/el-get/el-get")
  (unless (require 'el-get nil t)
    (url-retrieve
     "https://github.com/dimitri/el-get/raw/master/el-get-install.el"
     (lambda (s)
       (end-of-buffer)
       (eval-print-last-sexp))))
  (el-get 'sync)
  )

(defun load-ace-jump ()
  "load ace jump"
  (add-to-list 'load-path "which-folder-ace-jump-mode-file-in/")
  (require 'ace-jump-mode)
  (define-key global-map (kbd "C-c SPC") 'ace-jump-mode)
  )


(defun set-python-var ()
  "set python variable"
  (setq python-check-command "python3 /usr/local/bin/pyflakes")
  (setq
   python-shell-interpreter "ipython"
   python-shell-interpreter-args ""
   python-shell-prompt-regexp "In \\[[0-9]+\\]: "
   python-shell-prompt-output-regexp "Out\\[[0-9]+\\]: "
   python-shell-completion-setup-code
   "from IPython.core.completerlib import module_completion"
   python-shell-completion-module-string-code
   "';'.join(module_completion('''%s'''))\n"
   python-shell-completion-string-code
   "';'.join(get_ipython().Completer.all_completions('''%s'''))\n")
  )


(defun show-ip-info
    (host) "show ip information"
    (interactive "sHost:")
    (message (mapconcat
	      (lambda (i)
		(concat
		 (symbol-name (car i)) ": " (cdr i)))
	      (unless
		  (not (require 'json))
		(json-read-from-string
		 (let
		     ((out
		       (shell-command-to-string
			(concat "curl http://ipinfo.io/" host)
			)
		       ))
		   (substring
		    out
		    (string-match "{" out)
		    (1+
		     (string-match "}" out)
		     )
		    )
		   ))) "\n")))


(defun load-all ()
  "load all"
  (customize-color)
  (set-default-language)
  (set-frame-title)
  (set-python-var)
  (set-exec-path)
  (enable-line-column)
  (load-el-get)
  (dolist (package package-list) (el-get-install package))
  (load-ido)
  (load-undo-tree)
  (load-multiple-cursor)
  (load-jedi)
  (load-ace-jump)
  (set-markdown)
  (load-projectile)
  (load-git-emacs)
  (load-fill-indicator)
)

(load-all)

(provide 'emacs-startup)
