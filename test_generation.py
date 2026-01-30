from src.generation.answer_generator import AnswerGenerator

generator = AnswerGenerator()

query = "What is the name of author of book the alchemist ?"

answer = generator.generate_answer(query)

print("\nANSWER:\n")
print(answer)
