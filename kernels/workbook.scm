;; Minimal XLSL workbook runtime primitives
(define (workbook name version namespace)
  (list 'workbook name version namespace))

(define (pipeline . stages)
  stages)

(define (state . fields)
  fields)
