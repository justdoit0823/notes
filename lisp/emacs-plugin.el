;; This is a collection of my own emacs lisp plugin.


(defun git--check-python-syntax (filename)
  "check python file syntax in git repository"
  (unless (not (and (file-exists-p filename) (equal (file-name-extension filename) "py")))
    (let
	((ret (shell-command-to-string
	       (concat "python3 /usr/local/bin/pyflakes "
		       (git--get-top-dir) filename))))
      (when (> (length ret) 0) (error ret)))))


;; check added python file syntax
(defun git--check-added ()
  "check added files"
  (dolist (filename
	   (split-string
	    (git--exec-string "diff" "--cached" "--name-only") "[\n]+"))
    (git--check-python-syntax filename)))


;; check modified python file syntax
(defun git--check-modified ()
  "check modified files"
  (dolist (file (git--ls-files "-m"))
    (let ((filename (git--fileinfo->name file)))
      (git--check-python-syntax filename))))




(defun py-check-with-git ()
  "check python modified code in git repository"
  (dolist (file (git--ls-files "-m"))
    (let ((filename (git--fileinfo->name file)))
      (unless (not (and (file-exists-p filename) (equal (file-name-extension filename) "py")))
	(let
	    ((ret (shell-command-to-string
		   (concat "python /usr/local/bin/pyflakes "
			   (git--get-top-dir) filename))))
  	  (if (> (length ret) 0) (error ret) (message "pass check")))))))

(defun insert-line-next ()
  "insert line next"
  (interactive)
  (progn
    (move-beginning-of-line 2)
    (open-line 1)))


(provide 'emacs-plugin)
