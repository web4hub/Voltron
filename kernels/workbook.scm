;; AuraXLSL runtime bridge
(define pipeline '(observe encode retrieve reason plan execute store))
(define (workbook-entry runtime input) (runtime 'run input))
