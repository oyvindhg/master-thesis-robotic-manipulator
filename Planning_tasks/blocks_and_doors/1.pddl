(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
  (:objects
	L1 L2 L3 - location
	B1 - block
  )

  (:init
	(m-at L3)
	(free-grippers)
	(adjacent L1 L2)(adjacent L2 L1)
	(adjacent L2 L3)(adjacent L3 L2)
	(b-at B1 L1)
	(onground B1)(clear B1)
	(empty L2)
	(empty L3)
  )

  (:goal 
	(and(b-at B1 L3))
  )
)
