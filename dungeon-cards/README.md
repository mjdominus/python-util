# Implementation of Android "dungeon cards" game

The main goal is to build a simulator that can advise on strategy.

## Questions

Say the player wants to move to square L.  Who is responsible for deciding if they can?
I think it must be the board, which can actually install them there and then shuffle the other cards.
The board may of course ask the card already at L if it is going away.

Maybe the sequence is:
1. move-generator tells board that player wants to move to L
2. board notifies card at L that it has been attacked
3. Card performs some action but might call snuff().  
   At this point the board removes the card from the board, leaving None
   Card action returns
4. Board sees that L is now empty, moves player and refills board
   (Or, doesn't.)
   