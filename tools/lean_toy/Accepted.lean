theorem triangle_two_colours :
    ∀ a b c : Bool, a ≠ b → b ≠ c → a ≠ c → False := by
  decide
