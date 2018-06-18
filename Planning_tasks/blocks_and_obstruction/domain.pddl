;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Description
;;; ------------
;;; A manipulator works in an environment in
;;; which it might be obstructed. If obstructed
;;; it needs to handle the obstruction first.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (domain MANIPULATOR)
  (:requirements :strips :typing)
  (:types manipulator			;This is the robot that can be controlled
	  block				;This is the object that is supposed to be manipulated
	  obstruction			;This is an object that should not be here
	  location			;Location at which obstruction is safe
  )

  (:predicates (m-at ?m - manipulator ?l - location)
	       (holding-o ?m - manipulator ?o - obstruction)
	       (o-at ?o - obstruction ?l - location)
 	       (holding-b ?m - manipulator ?b - block)
	       (b-at ?b - block ?l - location)
	       (empty ?m - manipulator)
	       (safe ?l - location)
  )

  (:action move
	     :parameters (?m - manipulator ?from ?to - location)
	     :precondition (m-at ?m ?from)
	     :effect
		(and (m-at ?m ?to)
		(not(m-at ?m ?from)))
  )


  (:action pick-up-obstr
	     :parameters (?m - manipulator ?o - obstruction ?l - location)
	     :precondition (and (m-at ?m ?l)(o-at ?o ?l)(empty ?m))
	     :effect
		(and (holding-o ?m ?o)
		(not(empty ?m))
		(not(o-at ?o ?l)))
  )

  (:action put-down-obstr
	     :parameters (?m - manipulator ?o - obstruction ?l - location)
	     :precondition (and (m-at ?m ?l)(holding-o ?m ?o))
	     :effect
	        (and (empty ?m)
		(not(holding-o ?m ?o))
		(o-at ?o ?l))
  )

  (:action pick-up-block
	     :parameters (?m - manipulator ?b - block ?o - obstruction ?l1 ?l2 - location)
	     :precondition (and (m-at ?m ?l1)(b-at ?b ?l1)(safe ?l2)(o-at ?o ?l2)(empty ?m))
	     :effect
		(and (holding-b ?m ?b)
		(not(b-at ?b ?l))
		(not(empty ?m)))
  )

)
