;; Namespace router
(define routes
  '((cortex . "braneworld.cortex")
    (memory . "braneworld.hippocampus")
    (synapse . "braneworld.synapse")
    (vision . "workbook/Vision.workbook.xlsl")
    (world . "workbook/WorldModel.workbook.xlsl")))

(define (route name)
  (assoc name routes))
