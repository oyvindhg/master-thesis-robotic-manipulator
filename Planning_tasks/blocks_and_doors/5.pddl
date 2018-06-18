(define (problem MANIPULATOR-1)

(:domain MANIPULATOR)
  (:objects
	L1 L2 L3 - location
	B1 B2 B3 B4 B5 - block
  )

  (:init
	(m-at L3)
	(free-grippers)
	(adjacent L1 L2)(adjacent L2 L1)
	(adjacent L2 L3)(adjacent L3 L2)
	(b-at B1 L1)(b-at B2 L1)(b-at B3 L1)
	(onground B1)(on B2 B1)(on B3 B2)(clear B3)
	(b-at B4 L2)
	(onground B4)(clear B4)
	(b-at B5 L3)
	(onground B5)(clear B5)
  )

  (:goal 
	(and(b-at B1 L3)
	(on B2 B1)
	(on B3 B2)
	(on B4 B3)
	(on B5 B4))
  )
)
