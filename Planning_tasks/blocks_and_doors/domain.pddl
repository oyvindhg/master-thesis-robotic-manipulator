;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Description
;;; ------------
;;; A manipulator works in an environment in
;;; which...
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain MANIPULATOR)
  (:requirements :strips :typing)
  (:types block				;This is the object that is supposed to be manipulated
	  door				;This can be opened or closed
	  location			;Location at which obstruction is safe
  )

  (:predicates (m-at ?l - location)
	       (b-at ?b - block ?l - location)
	       (d-at ?d - door ?l1 ?l2 - location)
	       (adjacent ?l1 ?l2 - location)
 	       (holding ?b - block)
	       (on ?b1 ?b2 - block)
	       (onground ?b - block)
	       (clear ?b - block)
	       (empty ?l - location)
	       (free-grippers)
  )

  (:action move
	     :parameters (?from ?to - location)
	     :precondition 
		(and (m-at ?from)
		(adjacent ?from ?to))
	     :effect
		(and (m-at ?to)
		(not(m-at ?from)))
  )


  (:action place
	     :parameters (?b - block ?l - location)
	     :precondition 
		(and (m-at ?l)
		(empty ?l)
		(holding ?b))
	     :effect
	        (and (free-grippers)
		(not(holding ?b))
		(b-at ?b ?l)
		(clear ?b)
		(not(empty ?l))
		(onground ?b))
  )


  (:action stack
	     :parameters (?btop ?bbottom - block ?l - location)
	     :precondition 
		(and (m-at ?l)
		(b-at ?bbottom ?l)
		(clear ?bbottom)
		(holding ?btop))
	     :effect
	        (and (free-grippers)
		(not(holding ?btop))
		(b-at ?btop ?l)
		(on ?btop ?bbottom)
		(not(clear ?bbottom))
		(clear ?btop))
  )


  (:action pickup
	     :parameters (?b - block ?l - location)
	     :precondition 
		(and (m-at ?l)
		(b-at ?b ?l)
		(onground ?b)
		(clear ?b)
		(free-grippers))
	     :effect
		(and (holding ?b)
		(not(b-at ?b ?l))
		(not(free-grippers))
		(not(onground ?b))
		(empty ?l)
		(not(clear ?b)))
  )

  (:action destack
	     :parameters (?btop ?bbottom - block ?l - location)
	     :precondition 
		(and (m-at ?l)
		(b-at ?btop ?l)
		(b-at ?bbottom ?l)
		(clear ?btop)
		(on ?btop ?bbottom)
		(free-grippers))
	     :effect
		(and (holding ?btop)
		(not(b-at ?btop ?l))
		(not(free-grippers))
		(not(on ?btop ?bbottom))
		(not(clear ?btop))
		(clear ?bbottom))
  )


  (:action open
	     :parameters (?d - door ?unlockable ?locked - location)
	     :precondition 
		(and (m-at ?unlockable)
		(d-at ?d ?unlockable ?locked)
		(free-grippers))
	     :effect
		(and (adjacent ?unlockable ?locked)
		(adjacent ?locked ?unlockable))
  )

)
