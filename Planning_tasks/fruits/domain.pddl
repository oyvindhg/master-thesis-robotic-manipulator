;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;; Description
;;; ------------
;;; A manipulator works in an environment in
;;; which fruits can be moved around. There
;;; are also bowls into which fruits can be placed.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain FRUIT)
  (:requirements :strips :typing)
  (:types fruit
	  bowl
  )

  (:predicates (ontable ?f - fruit)
	       (empty ?b - bowl)
	       (inbowl ?f - fruit ?b - bowl)
	       (on ?f1 ?f2 - fruit)
	       (ontop ?f - fruit)
  )

  (:action insertfirst
	     :parameters (?f - fruit ?b - bowl)
	     :precondition 
		(and (empty ?b)
		(ontable ?f))
	     :effect
		(and (inbowl ?f ?b)
		(ontop ?f)
		(not(ontable ?f))
		(not(empty ?b)))
  )

  (:action stack
	     :parameters (?ftop ?fsecond - fruit ?b - bowl)
	     :precondition 
		(and (inbowl ?fsecond ?b)
		(ontop ?fsecond)
		(ontable ?ftop))
	     :effect
		(and (inbowl ?ftop ?b)
		(ontop ?ftop)
		(on ?ftop ?fsecond)
		(not(ontable ?ftop))
		(not(ontop ?fsecond)))
  )


  (:action destack
	     :parameters (?ftop ?fsecond - fruit ?b - bowl)
	     :precondition 
		(and (inbowl ?ftop ?b)
		(inbowl ?fsecond ?b)
		(ontop ?ftop)
		(on ?ftop ?fsecond))
	     :effect
		(and (ontop ?fsecond)
		(not(on ?ftop ?fsecond))
		(not(ontop ?ftop))
		(not(inbowl ?ftop ?b))
		(ontable ?ftop))
  )

  (:action removelast
	     :parameters (?f - fruit ?b - bowl)
	     :precondition 
		(and (inbowl ?f ?b)
		(ontop ?f))
	     :effect
		(and (not(ontop ?f))
		(not(inbowl ?f ?b))
		(ontable ?f)
		(empty ?b))
  )

)
