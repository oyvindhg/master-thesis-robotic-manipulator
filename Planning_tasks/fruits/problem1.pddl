(define (problem FRUIT-1)

(:domain FRUIT)
	(:objects
		bowl5 - bowl
		apple6 - fruit
		banana7 - fruit
		apple8 - fruit
		banana9 - fruit
	)

	(:init
		(inbowl banana9 bowl5)
		(ontop banana9)
		(ontable apple6)
		(ontable banana7)
		(ontable apple8)
	)

	(:goal
		(and
		(inbowl banana9 bowl5)
		(inbowl banana7 bowl5)
		(on banana7 banana9)
		(inbowl apple6 bowl5)
		(on apple6 banana7)
		(inbowl apple8 bowl5)
		(on apple8 apple6)
		)
	)
)