
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
    print("3. View statistics")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        name = input("Problem name: ").strip()

        if name == "":
            print("Problem name cannot be empty.")
            continue

        platform = input("Platform: ").strip()
        topic = input("Topic: ").strip()
        difficulty = input("Difficulty (Easy/Medium/Hard): ").strip().capitalize()

        if difficulty not in ["Easy", "Medium", "Hard"]:
            print("Invalid difficulty. Please enter Easy, Medium, or Hard.")
            continue

        problem = {
            "name": name,
            "platform": platform,
            "topic": topic,
            "difficulty": difficulty,
            "solved": False
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
        total = len(problems)
        easy = 0
        medium = 0
        hard = 0
        topics = {}

        for problem in problems:
            difficulty = problem["difficulty"].lower()

            if difficulty == "easy":
                easy += 1
            elif difficulty == "medium":
                medium += 1
            elif difficulty == "hard":
                hard += 1

            topic = problem["topic"].strip().title()

            if topic == "":
                topic = "Unspecified"

            if topic in topics:
                topics[topic] += 1
            else:
                topics[topic] = 1

        print("\n===== Statistics =====")
        print("Total problems:", total)
        print("Easy:", easy)
        print("Medium:", medium)
        print("Hard:", hard)

        print("\n===== Topic Statistics =====")

        if len(topics) == 0:
            print("No topics recorded yet.")
        else:
            for topic, count in topics.items():
                print(topic + ":", count)

    elif choice == "4":
        print("Keep coding. Keep improving!")
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, or 4.")