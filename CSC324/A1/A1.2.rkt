#lang racket #| CSC 324 - 2017 Fall - Assignment 1 - Part 2 / 2 |#

#| Due Saturday October 28th at Noon.
   May be done with one other student in the course. |#

#| ★ Implement ‘Eva’, a memory model based interpreter for an augmented Lambda Calculus.

 The syntactic language of Terms is the same as in Part 1, except for (add1 <term>).

 A run-time value is one of:
   • a number
   • a closure: (closure: (λ (<id>) <body>) <environment>)
     - a list containing the symbol closure:, a λ term, and an environment
   • an address of a closure

 An environment is a list of two-element lists: ((<id> <value>) ...).
   Earlier <id>s are more local than later ones, i.e. they shadow later ones.
   The <value>s are numbers or addresses.

 The model maintains a table associating addresses to closures.
 
 The semantics of function call is still eager by-value, with arguments passed by augmenting
  an environment.

   (<f> <a>)
     1. Evaluate <f> in the current environment, assume it produces an address of a closure c.
     2. Evaluate <a> in the current environment.
     3. Produce the value of the body of the λ term in c, evaluated in the environment of c
         augmented with a local variable associating the λ term's parameter with the value of <a>.

   (λ (<id>) <body>)
     1. Create a new closure with a new address, containing this λ term and current environment.
     2. Add the association of the address with the closure to the table of closures.
     3. Produce the address of the closure.

   <id>
     1. Produce the most local value of <id> from the current environment.

   <number>
     1. Produce the number. |#

(provide Eva)

#| Support library. |#

(define (lookup key table)
  (second (first (filter (λ (binding) (equal? (first binding) key)) table))))

(define (addresses)
  (define n -1)
  (λ () (local-require (only-in racket/syntax format-symbol))
    (set! n (add1 n))
    (format-symbol "λ~a" n)))

(module+ test
  (require rackunit)
  
  (check-equal? (lookup 'a '((b c) (a d) (a e))) 'd)

  (define generate-address (addresses))
  (check-equal? (generate-address) 'λ0)
  (check-equal? (generate-address) 'λ1))


#| Design and testing for Eva. |#

(module+ test
  
  ; An example, that is much too complicated for the first test in test-driven development.
  (check-equal? (Eva '((λ (x) (λ (y) x))
                       (λ (y) 324)))
                '(λ2 ; Result value.
                  ; Table associating addresses to closures.
                  ((λ2 (closure: (λ (y) x) ((x λ1))))
                   (λ1 (closure: (λ (y) 324) ()))
                   (λ0 (closure: (λ (x) (λ (y) x)) ())))))

  ; Your design and tests:
  
  ;(Eva <literal>)
  (check-equal? (Eva 1) '(1 ()))

  ;(Eva <id>)
  ; Shouldn't be done with empty environment.
  #;(check-equal? (Eva 'x) '(x ()))

  ;(Eva (λ (<id>) <a-term>))
  (check-equal? (Eva '(λ (x) 1))
                '(λ0 
                  ((λ0 (closure: (λ (x) 1) ())) )))

  (check-equal? (Eva '(λ (x) (λ (x) 1)))
                '(λ0 
                     ((λ0 (closure: (λ (x) (λ (x) 1)) ()) )) ))

  (check-equal? (Eva '(λ (x) ((λ (y) y) x)) )
                '(λ0
                     ((λ0 (closure: (λ (x) ((λ (y) y) x)) () )))))
  

  ;(Eva (f-term a-term))
  (check-equal? (Eva '((λ (x) 1) 7))
                '(1 ((λ0 (closure: (λ (x) 1) ()))))  )


  (check-equal? (Eva '((λ (x) 1)  (λ (x) 2)))
                '(1
                  ((λ1 (closure: (λ (x) 2) () ))
                    (λ0 (closure: (λ (x) 1) () )))))


  (check-equal? (Eva '((λ (x) x) 324))  '(324 ((λ0 (closure: (λ (x) x) () )))) )
  (check-equal? (Eva '((λ (x) x) (λ (x) 2))) '(λ1 ((λ1 (closure: (λ (x) 2) ()))
                                                   (λ0 (closure: (λ (x) x) ()))))  )

  (check-equal? (Eva '((λ (x) (λ (x) x) ) 123))   '(λ1 ((λ1 (closure: (λ (x) x) ((x 123))))
                                                        (λ0 (closure: (λ (x) (λ (x) x)) () )))))

  
  (check-equal? (Eva '((λ (x) (λ (y) y)) 123)) '(λ1 ((λ1 (closure: (λ (y) y) ((x 123))) )
                                                    (λ0 (closure: (λ (x) (λ (y) y)) ())) ))) 

  (check-equal? (Eva '((λ (x) (λ (x) x)) (λ (x) x))) '(λ2 ((λ2 (closure: (λ (x) x) ((x λ1))))
                                                           (λ1 (closure: (λ (x) x) ()))
                                                           (λ0 (closure: (λ (x) (λ (x) x)) ())))))
  
  (check-equal? (Eva '((λ (x) (λ (y) x)) (λ (x) x) ))  '(λ2 ((λ2 (closure: (λ (y) x) ((x λ1))))
                                                              (λ1 (closure: (λ (x) x) ()))
                                                              (λ0 (closure: (λ (x) (λ (y) x)) ())))))
  ;                       0      3          1         2
  (check-equal? (Eva '((λ (x) (λ (x) x)) ((λ (x) x) ((λ (y) y) 123)  )))
                  '(λ3 ((λ3 (closure: (λ (x) x) ((x 123))))
                       (λ2 (closure: (λ (y) y) ()))
                       (λ1 (closure: (λ (x) x) ()))
                       (λ0 (closure: (λ (x) (λ (x) x)) ()))
                       )))

  ;Ex5 pt2
  (check-equal? (Eva '((λ (One)
                         ((λ (Add1)
                            (Add1 (Add1 One)))
                          (λ (f) (λ (g) (λ (h) (g ((f g) h)))))))
                       (λ (h) h)))

                '(λ5 ((λ5 (closure: (λ (g) (λ (h) (g ((f g) h))))
                                    ((f λ4) (One λ1))))
    
                      (λ4 (closure: (λ (g) (λ (h) (g ((f g) h))))
                                    ((f λ1) (One λ1))))
    
                      (λ3 (closure: (λ (f) (λ (g) (λ (h) (g ((f g) h)))))
                                    ((One λ1))))
    
                      (λ2 (closure: (λ (Add1) (Add1 (Add1 One)))
                                    ((One λ1))))
    
                      (λ1 (closure: (λ (h) h) ()))
    
                      (λ0 (closure: (λ (One)
                                      ((λ (Add1)
                                         (Add1 (Add1 One)))
                                       (λ (f) (λ (g) (λ (h) (g ((f g) h)))))))
                                    ())))))
  

  )

(define (Eva term)

  (define generate-address (addresses))
  
  (define closures '())
  
  (define (eva term env)
    (match term
      [`(,f ,a) (define λaddress (eva f env));Evaluate f, return the address of closure for f
                (define λclosure (lookup λaddress closures)) ;The closure for f
                (define body (last (second λclosure))) ;The body of f
                (define λclosure-env (third λclosure)) ;The environment of the closure
                (define var (first(second (second λclosure)))) ; The parameter variable symbol.

                ;Evaluating a
                (define a-val (eva a env))

                ;Evaluate the body in the same environment as the closure, but with (var,a-val) added.
                (eva body (list* (list var a-val) λclosure-env))]

      [`(λ (,id) ,body) (define λi (generate-address))
                        (set! closures (list* (list λi `(closure: (λ (,id) ,body) ,env)) closures))
                        λi]

      ;<id>
     ;1. Produce the most local value of <id> from the current environment.
      
      [_ (cond [(symbol? term) (lookup term env)] ;Assume that term is in env at least once.
               [else term])]))

  
  (list (eva term '()) ; The value of term, in an empty initial environment.
        ; The table associating addresses to closures.
        closures))
