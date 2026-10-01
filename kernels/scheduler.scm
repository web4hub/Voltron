;; Deterministic bounded scheduler
(define (schedule queue horizon)
  (take queue (min horizon (length queue))))
