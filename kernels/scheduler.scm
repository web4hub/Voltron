;; Cooperative cognitive scheduler
(define (schedule tasks budget)
  (if (or (null? tasks) (<= budget 0))
      '()
      (cons (car tasks)
            (schedule (cdr tasks) (- budget 1)))))
