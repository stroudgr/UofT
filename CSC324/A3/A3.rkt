#lang racket #| CSC 324 2017 Fall Assignment 3  |#

#| A Type Checker with some Inference |#

(provide type) ; Implement ‘type’.


#| The Language of Types.

 Base types: Boolean, Number, String, Void, and ⊥ [called “bottom”, \bot].
   • Represented by symbols with those names.

 Function type constructor: (<Type> ... → <Type>)
   • Represented by a list of zero or more types, followed by the symbol →, followed by a type. |#


#| The Syntactic Language of Expressions.

 <base-literal> - represented by a boolean, number, or string.

 <identifier> - represented by a symbol.

 For each of the following, a list with that structure, where ‘...’ means zero or more of the
  preceding component, parts in angle-brackets are from the corresponding category, and other
  non-list components appear literally as symbols. Except: <Type> is never ⊥.

 (λ ((<identifier> : <Type>) ...)
   <body-expression>
   ...
   <result-expression>)

 (let ([<identifier> <expression>] ...)
    <body-expression>
    ...
    <result-expression>)

 (rec (<function-identifier> (<identifier> : <Type>) ... : <result-Type>)
   <body-expression>
   ...
   <result-expression>)
 
 (<function-expression> <argument-expression> ...)

 (if <condition-expression>
     <consequent-expression>
     <alternative-expression>)

 (set! <identifier> <expression>) |#

#| The Type of an Expression.

 As with evaluation, the type of an expression is relative to a current environment that contains
  a mapping of variables in scope to their types.
 Also, if at any point a type during the check of an expression is ⊥, the type of the whole expression
  is ⊥, and the expression is said to “not type check”.

 <base-literal> : the corresponding base type

 <identifier> : the type of the most local identifier with that name in the environment

 (λ ((<identifier> : <Type>) ...)
   <body-expression>
   ...
   <result-expression>)

   • In the current environment with each <identifier> bound locally to its corresponding <Type>:
      if each <body-expression> type checks then the type is (<Type> ... → <Result-Type>),
      where <Result-Type> is the type of <result-expression>.

 (let ([<identifier> <expression>] ...)
    <body-expression>
    ...
    <result-expression>)

   • If <expression> ... type check as <Type> ..., then the type is the same as the type of:

       ((λ ((<identitifer> : <Type>) ...)
          <body-expression>
          ...
          <result-expression>)
        <expression> ...)

 (rec (<function-identifier> (<identifier> : <Type>) ... : <result-Type>)
   <body-expression>
   ...
   <result-expression>)

   • In the current environment with <function-identifier> bound locally to <result-Type>,
      the type is the same as the type of:
       (λ ((<identitifer> : <Type>) ...)
         <body-expression>
         ...
         <result-expression>)

 (<function-expression> <argument-expression> ...)

   • Type checks iff the type of <function-expression> is a function type and the types of
      <argument-expression> ... match the function type's argument types, in which case
      the type is the function type's result type.

 (if <condition-expression>
     <consequent-expression>
     <alternative-expression>)

   • Type checks iff the type of the condition is Boolean, and the consequent and alternative
      have the same type, in which case the type of the expression is the type of the consequent.

 (set! <identifier> <expression>)

   • Type checks iff the type of the most local identifier with that name in the environment
      is the type of <expression>, in which case the type is Void. |#

; type : Expression → Type
; You may choose whatever representation for the environment that you like.


;------------------------------------------------------------------------------------------------

; Evaluates the list of expressions L in the environement env
; And returns whether or not any of them return '⊥
  (define (contains⊥? env L)
    (not (empty? (filter (λ (x) (equal? x '⊥))
                         (map
                          (λ (ele)
                            (type ele env))
                          L)))))


(define (type expr [env '()])  
  (match expr
    ;-------------------------------------------------------------
    ; Ensure the type of c is Boolean, and both t and f are the same type. If so return type of t/f
    ; Otherwise don't type check.
    [`(if ,c ,t ,f) (cond [(and (equal? (type c env) 'Boolean)
                                (equal? (type t env) (type f env)))
                           (type f env)]
                          [else '⊥])]
    ;-----------------------------------------------------------------
    ;
    [`(let ([,id ,expr] ...) ,body ... ,res)
     ; Ensure all expr's types are not '⊥
     (cond [(contains⊥? env expr) '⊥]
           [else
            ; Types of all the expr's
            (define exprTypes (map (λ (ele) (type ele env)) expr))
            ;(println exprTypes)

            ; What let expands to
            (define expansion (append
                               (list (append
                                      `(λ ,(map list id (map (λ (x) ':) id) exprTypes))
                                      body 
                                      (list res)))
                               expr))
            ;(println expansion)
            ; Call on the expansion
            (type expansion env)])]
    ;------------------------------------------------------------------
    [`((λ ((,id : ,idType) ...) ,body ... ) ,args ...)

     ; Gets the types of the inputs
     (define argsRes
       (map (λ (ele) (type ele env)) args))

     ; Gets all (id, idType) pairs
     (define pairs (map list id (map (λ (x) ':) id) idType))

     ; Evaluate the type of the function
     (define funRes (type (append (append `(λ ,pairs) body )) env ))
     
     (match funRes
       ['⊥ '⊥]
       ; Ensure the arguments passed match the type of the function
       ; Return the output type of the function
       [`(,input ... → ,out) (cond [(equal? input argsRes) out][else '⊥])]
       [_ '⊥])]
    ;--------------------------------------------------------------------
    
    [`(rec (,f-id (,id : ,idType) ... : ,result-type) ,body ... ,result)

     ; (id idType) pairs
     (define pairs (map list id (map (λ (x) ':) id) idType))
     (define expansion (append `(λ ,pairs) body (list result)))

     ;************************************************************************
     ; NOTE: Two ways to interpret the type of f-id.
     ; One option: f-id has type (specified by instructions)
     (define f-type result-type)
     ; Another option: f-id has type (what I felt was more natural)
     ; https://piazza.com/class/j7azb9w9yrb4ub?cid=329
     #;(define f-type (append idType '(→) (list result-type)))
     ;****************************************************************
     
     (define newEnv (list* (list f-id f-type) env))
     ;(println newEnv)
     (type expansion newEnv)]
    
    ;---------------------------------------------------------------------
    ;(set! <identifier> <expression>)
    ;Type checks iff the type of the most local identifier with that name in
    ;the environment
    ; is the type of <expression>, in which case the type is Void. 

    [`(set! ,id ,value) (define L (filter
                                 (λ (e) (equal? (type id env) (second e)))
                                 (lookup id env)))
                        (cond
                          [(empty? L) '⊥]
                          [(equal? (second (first L))  (type value env)) 'Void]
                          [else '⊥])]

    
    ;---------------------------------------------------------------------
    [`(λ ((,x : ,xtype)...) ,body ... ,res)
     ; Creates the new environement where x = xtype
     (define newEnv (append (map list x xtype) env))
     (define result (type res newEnv))
     #;(println (map (λ (ele)
                       (type ele env))
                     body))
     (cond [(or (equal? result '⊥)
                (contains⊥? newEnv body)) '⊥]
           [else (append xtype
                         (list '→ result))])]
    ;----------------------------------------------------------------------
    [`(,f ,args ...) 
     ; Evaulate the types of the arguments
     (define argsRes
       (map (λ (ele) (type ele env)) args))
     ; Evaluate the type of the function
     (define funRes (type f env))

     (match funRes
       ['⊥ '⊥]
       ; Ensure the arguments passed match the type of the function
       ; Return the output type of the function
       [`(,input ... → ,out) (cond [(equal? input argsRes) out][else '⊥])]
       [_ '⊥])]
    
    ;----------------------------------------------------------------------
    [some (cond [(number? some) 'Number]
                [(boolean? some) 'Boolean]
                [(string? some) 'String]
                [(equal? some 'add1) '(Number → Number)] ; Example for testing (type '(add1 3))
                [(equal? some '⊥) '⊥]
                [(equal? some ''⊥) '⊥] ; I've often done testing with body= '('⊥ ...) when I meant body= '(⊥ ...) 
                [(symbol? some) (define L (lookup some env))
                                (cond [(empty? L) '⊥] [else (second (first L))])]
                [else '⊥])]))

; env = '( (name type) ...    )

(define (lookup key table)
  (filter (λ (binding) (equal? (first binding) key)) table)  )
#;(define (lookup1 key table)
    (second (first (filter (λ (binding) (equal? (first binding) key)) table))))
;------------------------------------------------------------------------------------------------

#| TESTING |#

(module+ test (require rackunit)

  ;-------------------------------------------------------------------------------------------------
  ; Base cases
  (check-equal? (type 1) 'Number)
  (check-equal? (type "word") 'String)
  (check-equal? (type #t) 'Boolean)

  ;----------------------------------------------------------------------------------------------
  ; Symbols
  (check-equal? (type 'x (list (list 'x 'Number))) 'Number)
  (check-equal? (type 'x '((y Number)(x String) (x Number))) 'String)

  ;-------------------------------------------------------------------------------------------------
  ;(λ ((<identifier> : <Type>) ...) <body-expression> ... <result-expression>)
  (check-equal? (type '(λ ((x : Number) (y : String)) 1 2 x) ) '(Number String → Number))
  (check-equal? (type '(λ ((x : (Number → Number)) (y : String)) 1 2 x) ) '((Number → Number) String → (Number → Number)))
  (check-equal? (type '(λ ((x : Number) (y : String)) 1 2 (λ ((y : Number)) x))) '(Number String → (Number → Number)))
  (check-equal? (type '(λ ((x : (Number → Number))) (λ ((y : Boolean)) "ss")))
                '((Number → Number) → (Boolean → String)))

  ;------------------------------------------------------------------------------------------------
  ;(let ([<identifier> <expression>] ...) <body-expression> ... <result-expression>)
  (check-equal? (type '(let ((x 100) (y "str")) 1 2 y )) 'String)
  (check-equal? (type '(let ((x (λ ((y : Number)) y))
                             (y "str"))
                         1 2 x)) '(Number → Number))

  ;---------------------------------------------------------------------------------------------
  ;(rec (<function-identifier> (<identifier> : <Type>) ... : <result-Type>) <body-expression> ... <result-expression>)

  ;*******************************************************
  ; CASE: function-identifier bound to result-Type
  (check-equal? (type '(rec (fun (x : Number) (y : String) : String) 1 2 3 fun))
                '(Number String → String))
  ;CASE: function identifier bound to (Type ... → result-type)
  #; (check-equal? (type '(rec (fun (x : Number) (y : String) : String) 1 2 3 (fun 1 "s")))
                '(Number String → String))
  ;***************************************************************************
  ;----------------------------------------------------------------------------------------------
  ;(<function-expression> <argument-expression> ...)
  (check-equal? (type '((λ ((x : Number) (y : Number)) x y) 1 3)) 'Number)
  
  ;-----------------------------------------------------------------------------------------
  ;(if <condition-expression>    <consequent-expression>  <alternative-expression>)

  (check-equal? (type '(if #t 1 2)) 'Number)
  (check-equal? (type '(if #f 1 "s")) '⊥)
  
  ;-------------------------------------------------------------------------------------------
  ;(set! <identifier> <expression>) 
  (check-equal? (type '(set! x 80) '((x Number))) 'Void)
  (check-equal? (type '(set! x "s") '((x Number))) '⊥)

  )
