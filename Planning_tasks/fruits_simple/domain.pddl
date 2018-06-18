(define (domain FRUITS)

  (:requirements :strips :typing)
  (:types fruit
	  bowl)

  (:predicates
    (ontable ?f - fruit)
    (empty ?b - bowl)
    (inbowl ?f - fruit ?b - bowl))

  (:action insert
    :parameters
      (?f - fruit ?b - bowl)
    :precondition 
      (and (empty ?b)
      (ontable ?f))
    :effect
      (and (inbowl ?f ?b)
      (not(ontable ?f))
      (not(empty ?b))))

  (:action remove
    :parameters
      (?f - fruit ?b - bowl)
    :precondition 
      (inbowl ?f ?b)
    :effect
      (and (not(inbowl ?f ?b))
      (ontable ?f)
      (empty ?b)))
)
