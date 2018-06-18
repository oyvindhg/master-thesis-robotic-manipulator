(define (problem FRUITS-1)

  (:domain FRUIT)
    (:objects
      fruitbowl - bowl
      apple - fruit)

    (:init
      (empty fruitbowl)
      (ontable apple))

    (:goal
      (inbowl apple fruitbowl))
)
