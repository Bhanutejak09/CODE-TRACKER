
import json

try:
    with open("problems.json", "r") as file:
        problems = json.load(file)
except FileNotFoundError:
    problems = []

while True:
    print("\n===== CodeTrack =====")
    print("1. Add a problem")
    print("2. View problems")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Problem name: ")
        platform = input("Platform: ")
        topic = input("Topic: ")
        difficulty = input("Difficulty (Easy/Medium/Hard): ")

        problem = {
            "name": name,
            "platform": platform,
            "topic": topic,
            "difficulty": difficulty
        }

        problems.append(problem)

        with open("problems.json", "w") as file:
            json.dump(problems, file, indent=4)

        print("Problem saved successfully!")

    elif choice == "2":
        if len(problems) == 0:
            print("No problems recorded yet.")
        else:
            for problem in problems:
                print("\nProblem:", problem["name"])
                print("Platform:", problem["platform"])
                print("Topic:", problem["topic"])
                print("Difficulty:", problem["difficulty"])

    elif choice == "3":
        print("Keep coding. Keep improving!")
        break

    else:
        print("Invalid option. Try again.")
