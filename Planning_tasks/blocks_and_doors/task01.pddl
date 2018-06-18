(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
  (:objects
	D - door
	L1 L2 L3 L4 - location
	B1 B2 B3 B4 B5 B6 - block
  )

  (:init
	(m-at L1)
	(holding B4)
	(adjacent L1 L2)(adjacent L2 L1)
	(d-at D L2 L3)
	(adjacent L3 L4)(adjacent L4 L3)
	(b-at B1 L1)(b-at B2 L1)(b-at B3 L1)
	(onground B3)(on B2 B3)(on B1 B2)(clear B1)
	(b-at B6 L4)(b-at B5 L4)
	(onground B6)(on B5 B6)(clear B5)
	(empty L3)
  )

  (:goal 
	(and(b-at B3 L4)
	(on B2 B3))
  )
)
