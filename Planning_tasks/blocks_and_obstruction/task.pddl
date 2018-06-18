(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
(:objects
	  B - block
	  O - obstruction
	  M - manipulator
	  L1 L2 - location)

(:init
	  (m-at M L1)
  	  (b-at B L2)
  	  (o-at O L2)
  	  (safe L1)
  	  (empty M)
)

(:goal 
	  (holding-b M B)
)
)
