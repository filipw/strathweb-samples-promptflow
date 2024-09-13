from promptflow.core import tool

@tool
def fetch_classification_categories(category: str) -> list:
  if category.lower() == "quantum computing":
    return [
      "Quantum Algorithms",
      "Quantum Cryptography",
      "Quantum Hardware",
      "Quantum Error Correction",
      "Quantum Simulation"
    ]

  raise ValueError(f"Category '{category}' not recognized.")
