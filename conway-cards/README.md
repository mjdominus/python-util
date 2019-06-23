
Conway three-cards-in-a-pile puzzle

Three spots are marked on a table and three cards (and Ace, Deuce, and
Three) are placed face up at random, not necessarily all on different
spots.  Your task is to design an algorithm which moves the cards
until they are stacked up on the leftmost spot, with the Three on the
bottom and the Ace on the top, subject to the following constraints:

  1. The algorithm may move only one card at a time
  2. The algorithm must be entirely stateless
  3. The algorithm must be guaranteed to produce the desired
     configuration in a bounded amount of time.

Easier version: the cards may be stacked up on any of the three spots.
