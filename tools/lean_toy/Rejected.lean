theorem triangle_three_colours :
    ∀ a b c : Fin 3, a ≠ b → b ≠ c → a ≠ c → False := by
  decide
