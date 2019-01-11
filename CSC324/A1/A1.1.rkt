#lang racket #| CSC 324 - 2017 Fall - Assignment 1 - Part 1 / 2 |#

#| Due Saturday October 28th at Noon.
   May be done with one other student in the course. |#

#| ★ Implement ‘eva’, an algebraic interpreter for an augmented Lambda Calculus.

 The syntactic language of Terms is the Lambda Calculus, augmented with numeric literals
  and a special constant ‘add1’ that when called with a numeric literal adds one to it.

   (λ (<identifier>) <term>)
     - represented by a list containing:
       • the symbol λ
       • a list containing an identifier
       • a term
   (add1 <a-term>)
     - represented by a list containing the symbol add1, and a term
   (<f-term> <a-term>)
     - represented by a list containing two terms
   <identifier>
     - represented by a symbol
   <literal>
     - represented by a number

 The semantics of function call is eager by-value, by algebraic substitution.

   (add1 <a-term>)
     1. Evaluate <a-term>, assume it produces a numeric literal.
     2. Add one to the value of <a-term>.

   (<f-term> <a-term>)
     1. Evaluate <f-term>, assume it produces a λ term: (λ (<id>) <body>) .
     2. Evaluate <a-term>, producing a value v.
     3. Substitute v into <body> by replacing <id> in <body> with v.
        Respect scope: if <body> contains a λ term whose parameter is also <id>,
         do not replace <id> anywhere in that λ term.
     4. Evaluate the transformed body.

   Any other term.
     The value of the term is itself. |#

(provide eva sub)

(module+ test
  (require rackunit)
  
  ; An example, that is already too complicated for the first test in test-driven development.
  (check-equal? (eva '((λ (x) (add1 x)) 0)) 1)

  (check-equal? (sub 'x 0 '(λ (y) ((λ (x) x) x))) '(λ (y) ((λ (x) x) 0)))

  ; Your design and tests:

  (check-equal? (eva 2) 2)
  (check-equal? (eva 'a) 'a)
  
  (check-equal? (eva '(add1 1)) 2)
  (check-equal? (eva '(add1 (add1 0))) 2)
  (check-equal? (eva '(add1 ((λ (x) x) 2))) 3)

  ;(check-equal? (eva '(λ (id) term)) )
  (check-equal? (eva '(λ (id) 1)) '(λ (id) 1))
  (check-equal? (eva '(λ (id) (add1 1))) '(λ (id) (add1 1)))
  ;(check-equal? (eva '(λ (id) (add1 1))) '(λ (id) (add1 1)))

  ;(check-equal? (eva (f-term a-term) ))
  (check-equal? (eva '( (λ (id) 1) 2 ))  1)
  (check-equal? (eva '( (λ (id) (add1 id))  (add1 1)))  3)
  (check-equal? (eva '( (λ (id) (λ (x) 5)) 2))  '(λ (x) 5))
  (check-equal? (eva '( (λ (id) (λ (x) id)) 2)) '(λ (x) 2))
  (check-equal? (eva '((λ (id) ((λ (x) (add1 x)) 5)) 10 ))  6)

  ; (sub id value literal) 
  (check-equal? (sub 'x  4 1 ) 1)
  (check-equal? (sub 'y (add1 1) 2) 2)

  ; (sub id value identifier) 
  (check-equal? (sub 'x 3 'x) 3)
  (check-equal? (sub 'x 4 'y) 'y)
  (check-equal? (sub 'x '(λ (x) (add1 x)) 'x )  '(λ (x) (add1 x)))

  ;(sub id value (add1 a-term))
  (check-equal? (sub 'x 4 '(add1 4)) '(add1 4))
  (check-equal? (sub 'x 4 '(add1 ((λ (x) (add1 x)) 5) )) '(add1 ((λ (x) (add1 x)) 5) ))

  ;(sub id value (λ (x) a-term))
  (check-equal? (sub 'x 10 '(λ (y) x))  '(λ (y) 10))
  (check-equal? (sub 'x 10 '(λ (y) ((λ (x) (add1 x)) x))) '(λ (y) ((λ (x) (add1 x)) 10)))

  ;(sub id value (f-term a-term))
  (check-equal? (sub 'x 10 '((λ (y) x) 8))  '((λ (y) 10) 8)    )
  (check-equal? (sub 'x 10 '((λ (y) (add1 y)) (add1 x)))  '((λ (y) (add1 y)) (add1 10))    )
  (check-equal? (sub 'x 10 '((λ (x) x) x))  '((λ (x) x) 10)    )

  ;Invalid input, behaviour undefined
  #;(check-equal? (eva '(1 2)) '(1 2))
  
  )


(define (eva term)
  (match term
    [`(add1 ,a-term) (add1 (eva a-term))]

    ;These two are equivalent ways to deal with (eva (f-term a-term)).
    ;The first one asserts f-term is of the form (λ (x) term) by matching (simpler).
    ;The second one will actually evaluate f-term, then match it (semantics of function calls says to evaluate f-term).
    [`((λ (,x) ,body) ,a-term) (eva (sub x (eva a-term) body)) ]   
    [`(,f-term ,a-term)
     (match (eva f-term)
       [`(λ (,x) ,body) (eva (sub x (eva a-term) body))]
       [_ `(,f-term ,a-term)] ;Get here by calling something like (eva '(1 2)). '(1 2) is not a term.  
       )]
    
    [`(add1 ,a-term) (add1 (eva a-term))]
    [_ term] ;literals, symbols, and `(λ (,x) ,a-term)
    ))


#| ★ Implement algebraic substitution.

 sub : symbol Term Term → Term
 Substitute value for id in term, respecting scope. |#

(define (sub id value term)
  (define (sub′ e) (sub id value e))
  (match term
    [`(λ (,id′) ,body) (cond [(equal? id′ id) term] [else `(λ (,id′) ,(sub′ body))] )]
    [`(,f ,a) `(,(sub′ f) ,(sub′ a))]
    [`(add1 ,a) `(add1 ,(sub′ a))]
    [_ (cond [(equal? id term) value] [else term])]))
