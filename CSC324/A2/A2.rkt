#lang racket #| CSC324 2017 Fall Assignment 2 : Due Wednesday November 29 at 6PM. |#

#| The Maybe Monad.

 In this assignment you implement the functional API for computation that propagates false as failure,
  and use that to implement the associated Do notation. |#

(provide >> >>=
         ÷ √ ln
         E1 Do E2 E3)

(module+ test (require rackunit)
  
  ; Implement ‘>>’, called “then”, that takes two *expressions* and produces an expression that:
  ;   1. Evaluates the first expression.
  ;   2. If that produces false then that is the result.
  ;   3. Otherwise, evaluates the second expression and that is the result.

  (check-false (>> (not (zero? 0)) (/ 324 0)))
  (check-equal? (>> (not (zero? 324)) (/ 324 324))
                  1)
  (check-false (>> (number? "324") (>> (not (zero? "324")) (/ 324 "324"))))

  ; Implement functions ÷, √, and ln, that produce false if dividing by zero, taking the square root
  ;  of a negative number, or taking the logarithm of a non-positive number.
  ; Use ‘>>’ appropriately in the implementations.
  ; Implement ÷ curried: taking a number, and returning a unary function ready to divide a number.

  #;(check-false (√ -1))
  #;(check-equal? (√ 324) 18)
  #;(check-false ((÷ 1) 0))
  #;(check-equal? ((÷ 324) 18) 18)
  #;(check-false (ln 0))
  #;(check-equal? (ln 324) (log 324))
  
  ; Implement *function* ‘>>=’, called “bind”, that takes two arguments and:
  ;  1. If the first argument is false then that is the result.
  ;  2. Otherwise, calls the second argument on the first.
  ; Use ‘>>’ appropriately in the implementation.

  #;(check-false (>>= -1 √))
  #;(check-false (>>= (>>= -1 √) ln))
  #;(check-equal? (>>= (>>= (>>= 324 √) (÷ 1)) ln)
                  (log (/ (sqrt 324)))))

#;(define >> (λ (a) (cond [(not a) a] [else b])))

(define-syntax >>
    (syntax-rules ()
      [(>> a b) (cond [(not a) a] [else b])]))

(define ÷ (λ (a) (λ (b) (>> (not (zero? b)) (/ a b)))))
(define √ (λ (a) (>> (not (negative? a)) (sqrt a))))
(define ln (λ (a) (>> (positive? a) (log a))))
(define >>= (λ (a b) (>> a (b a))))

#;(define (÷ a) (λ (b) (>> (not (zero? b)) (/ a b))))
#;(define (√ a) (>> (not (negative? a)) (sqrt a)))
#;(define (ln a) (>> (positive? a) (log a)))
#;(define (>>= a b)
    (>> a (b a)))

; Consider this language of arithmetic expressions:
;   <numeric-literal>
;      - represented by a number
;   (√ <ae>)
;      - represented by a list with the symbol √  and an arithemtic expression
;   (ln <ae>)
;      - represented by a list with the symbol ln and an arithemtic expression
;   (<ae> ÷ <ae>)
;      - represented by a list with an arithmetic expression, symbol ÷, and arithemtic expression
  
; Implement function ‘E1’ to evaluate such expressions, producing false if any of the computations
;  are invalid according to the earlier restrictions for square root, logarithm, and division.
; Use pattern matching appropriately, along with ‘>>’ and ‘>>=’ for propagating false.
; In particular, do not use any other conditionals, nor boolean operations or literals.
; Use quasiquotation as appropriate for the patterns, but nothing else from match's pattern language
; [e.g. don't use ‘?’, nor #:when].
(define E1
  (λ (term)
    (match term
      [`(,a ÷ ,b) (>> (and (E1 a) (E1 b)) ( (÷ (E1 a)) (E1 b)) )]
      [`(√ ,a) (>> (E1 a) (√ (E1 a)))]
      [`(ln ,a) (>> (E1 a) (ln (E1 a)))]
      [_ term])))

(module+ test (require rackunit)

  (check-equal? (E1 1) 1)
  (check-equal? (E1 '(6 ÷ 3)) 2)
  (check-equal? (E1 '(√ 9)) 3)
  (check-equal? (E1 '(ln 1)) 0)

  (check-equal? (E1 '((6 ÷ 3) ÷ (10 ÷ 5))) 1)
  (check-equal? (E1 '((ln 36) ÷ (√ 4))) (log 6))
  (check-equal? (E1 '(√ ( ((√ 81) ÷ (√ 1))  ÷  (√ (1 ÷ 16)) )))  6)

  (check-false (E1 '(√ -1)))
  (check-false (E1 '(1 ÷ 0)))
  (check-false (E1 '(ln (ln 1))))
  (check-false (E1 '(√(9 ÷ (√(ln 0))))))
  
  )


; Implement ‘Do’, using ‘>>’ and ‘>>=’ appropriately.
;
; It takes a sequence of clauses to be evaluated in order, short-circuiting to produce false if any
;  of the clauses produces false, producing the value of the last clause.
;
; Except for the last clause, a clause can be of the form
#;(identifier ← expression)
;  in which case its meaning is: evaluate the expression, and make the identifier refer to the
;  value in subsequent clauses.
;
; Don't use any local naming [local, let, match, define, etc] except for λ parameters:
;  recall that ‘let’ is just a notation for a particular lambda calculus “design pattern”.
  
(module+ test
  (check-equal? (Do 324)
                  324)
  (check-false (Do #false
                     (/ 1 0)))
  (check-false (Do (r1 ← (√ -1))
                     (r2 ← (ln (+ 1 r1)))
                     ((÷ r1) r2)))
  (check-false (Do (r1 ← (√ -1))
                     (r2 ← (ln (+ 1 r1)))
                     ((÷ r1) r2))))

#;(define Do (λ args
               (cond [(empty? args) args]
                     [else (>>= first )])))

(define-syntax Do (syntax-rules (←)
                    [(Do (id ← value) rest ... )
                     (>>= value (λ (id) (Do rest ... )))]
                    [(Do value) value]
                    [(Do first rest ...) (>> first  (Do rest ...))]))

; Implement ‘E2’, behaving the same way as ‘E1’, but using ‘Do’ notation instead of ‘>>’ and ‘>>=’.

(define E2
  (λ (term)
    (match term
      #;[`(,a ÷ ,b) (>> (and (E2 a) (E2 b)) ( (÷ (E2 a)) (E2 b)) )]
      [`(,a ÷ ,b) (Do (r1 ← (E2 a)) (r2 ← (E2 b)) ((÷ r1) r2)) ]
      #;[`(√ ,a) (>> (E2 a) (√ (E2 a)))]
      [`(√ ,a) (Do (r1 ← (E2 a)) (√ r1))]
      #;[`(ln ,a) (>> (E2 a) (ln (E2 a)))]
      [`(ln ,a) (Do (r1 ← (E2 a)) (ln r1))]
      [_ term])))

; Implement ‘E3’, behaving the same way as ‘E2’, by expanding each use of ‘Do’ notation in ‘E2’,
;  and also replacing ‘E2’ with ‘E3’. The result will be similar to your ‘E1’, but likely a bit
;  less elegant.

(define E3
  (λ (term)
    (match term
      #;[`(,a ÷ ,b) (Do (r1 ← (E3 a)) (r2 ← (E3 b)) (÷ r1 r2)) ]
      [`(,a ÷ ,b) (>>= (E3 a)
                       (λ (r1) (>>= (E3 b)
                                    (λ (r2) ((÷ r1) r2)) )))] 
      #;[`(√ ,a) (Do (r1 ← (E3 a)) (√ r1))]
      [`(√ ,a) (>>= (E3 a) (λ (r1) (√ r1)))]
      #;[`(ln ,a) (Do (r1 ← (E3 a)) (ln r1))]
      [`(ln ,a) (>>= (E3 a) (λ (r1) (ln r1)))]
      [_ term])))

(module+ test (require rackunit)

  (check-equal? (E2 1) 1)
  (check-equal? (E2 '(6 ÷ 3)) 2)
  (check-equal? (E2 '(√ 9)) 3)
  (check-equal? (E2 '(ln 1)) 0)

  (check-equal? (E2 '((6 ÷ 3) ÷ (10 ÷ 5))) 1)
  (check-equal? (E2 '((ln 36) ÷ (√ 4))) (log 6))
  (check-equal? (E2 '(√ ( ((√ 81) ÷ (√ 1))  ÷  (√ (1 ÷ 16)) )))  6)

  (check-false (E2 '(√ -1)))
  (check-false (E2 '(1 ÷ 0)))
  (check-false (E2 '(ln (ln 1))))
  (check-false (E2 '(√(9 ÷ (√(ln 0))))))

  (check-equal? (E3 1) 1)
  (check-equal? (E3 '(6 ÷ 3)) 2)
  (check-equal? (E3 '(√ 9)) 3)
  (check-equal? (E3 '(ln 1)) 0)

  (check-equal? (E3 '((6 ÷ 3) ÷ (10 ÷ 5))) 1)
  (check-equal? (E3 '((ln 36) ÷ (√ 4))) (log 6))
  (check-equal? (E3 '(√ ( ((√ 81) ÷ (√ 1))  ÷  (√ (1 ÷ 16)) )))  6)

  (check-false (E3 '(√ -1)))
  (check-false (E3 '(1 ÷ 0)))
  (check-false (E3 '(ln (ln 1))))
  (check-false (E3 '(√(9 ÷ (√(ln 0))))))

  
  )
