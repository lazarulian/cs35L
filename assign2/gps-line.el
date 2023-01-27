(defun gps-line ()
  "Print the current location of the line in respect to the total number of lines in the buffer"
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos)))
		(setq total-lines (count-lines (window-start) (window-end)))
		(setq new-lines (how-many "\n" 0))
    (if (= start 1)
	(message "Line %d/%d" n new-lines)
      (save-excursion
	(save-restriction
	  (widen)
	  (message "line %d/%d (narrowed line %d)"
		   (+ n (line-number-at-pos start) -1) new-lines n))))))
