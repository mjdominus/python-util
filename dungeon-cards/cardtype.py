
card_library = {}

class cardtype():
  def __init__(self, name, action_dict):
    self.name = name
    self.actions = action_dict
    self.register()

  def register(self):
    if self.name in card_library:
      raise Exception("Conflict: card type '%s' already registered" % self.name)
    card_library[self.name] = self

cardtype("player", {})

# class playercard(cardtype):
#     def __init__(self):
#       super().__init__("player", {})
#

# self.actions = {"turn": [],  # Does this every turn
#                 "death": [],  # Does this when it dies
#                 "attacked": [],  # Does this when attacked
#                 "flamed": [],  # Does this when burnt
#                 "poisoned": [],  # Does this when poisoned
#                 "tick0": [],  # Does this when times runs out
