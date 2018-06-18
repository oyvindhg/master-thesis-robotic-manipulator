(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
  (:objects
	D - door
	L1 L2 L3 L4 - location
	B1 B2 - block
  )

  (:init
	(m-at L3)
	(holding B1)
	(adjacent L1 L2)(adjacent L2 L1)
	(adjacent L2 L3)(adjacent L3 L2)
	(d-at D L3 L4)
	(empty L1)
	(empty L4)
	(b-at B2 L2)
	(onground B2)(clear B2)
  )

  (:goal 
	(b-at B2 L4)
  )
)
