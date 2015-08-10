;; This is a fast def jump way in python module.

;; Author: justdoit

;; Email: justdoit920823@gmail.com

;; you can use like this:

;; 1. put this el file to your emacs load path

;; 2. add this code to your .emacs file

;; (require 'pydefjump)

;; (global-set-key (kdb "C-c d") 'jump-to-def)


(require 'epc)


(defvar-local pydef-path "~/.emacs.d/python_def_list_server.py")

(defvar def-epc (epc:start-epc "python" '(pydef-path . nil)))


(defun jump-to-def ()
  "fast way to jump to def position in python"
  (interactive)
  (let ((def-ret (epc:call-sync def-epc 'get_file_def_pos (cons (buffer-file-name) nil)))
	;; (def-keys (car def-ret))
	;; (def-map (cdr def-ret))
	;; (def-pos (plist-get def-map (completing-read "def name: " def-keys)))
	)
    (setq-local def-keys (car def-ret))
    (setq-local def-map (nth 1 def-ret))
    (setq-local def-name (completing-read "def name: " def-keys))
    (setq-local def-pos (plist-get def-map (intern (concat ":" def-name))))
    (goto-line (car def-pos)) (move-to-column (nth 1 def-pos))))


(provide 'pydefjump)
