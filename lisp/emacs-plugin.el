;; This is a collection of my own emacs lisp plugin.


(defun py-check-with-git ()
  "check python modified code in git repository"
  (dolist (file (git--ls-files "-m"))
    (let ((filename (git--fileinfo->name file)))
      (unless (not (equal (file-name-extension filename) "py"))
	(let
	    ((ret (shell-command-to-string
		   (concat "python /usr/local/bin/pyflakes "
			   (git--get-top-dir) filename))))
  	  (if (> (length ret) 0) (error ret) (message "pass check")))))))
