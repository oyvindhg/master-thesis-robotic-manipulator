(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
  (:objects
	L1 L2 L3 - location
	B - block
  )

  (:init
	(m-at L1)
	(free-grippers)
	(adjacent L1 L2)(adjacent L2 L1)
	(adjacent L2 L3)(adjacent L3 L2)
	(b-at B L2)
	(onground B)(clear B)
	(empty L3)
  )

  (:goal 
	(and(b-at B L3))
  )
)
