;; Voltron workbook router
(define routes '((perception . "braneworld/perception.py")
                 (cortex . "braneworld/cortex.py")
                 (memory . "braneworld/hippocampus.py")
                 (planner . "braneworld/planner.py")
                 (reasoning . "braneworld/reasoning.py")))

(define (route name) (assoc name routes))
