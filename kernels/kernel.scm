;; Voltron Braneworld kernel
(define (bounded x lo hi) (max lo (min hi x)))
(define (dispatch state event)
  (list 'dispatch state event))
