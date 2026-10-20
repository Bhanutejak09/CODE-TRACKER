
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
    print("4. Mark a problem as solved")
    print("5. Search & Filter")
    print("6. Exit")

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


                status = "Solved" if problem.get("solved", False) else "Not solved"
                print("Status:", status)
                

    elif choice == "3":
        total = len(problems)
        easy = 0
        medium = 0
        hard = 0
        solved = 0
        unsolved = 0
        topics = {}

        for problem in problems:
            if problem.get("solved", False):
                solved += 1
            else:
                unsolved += 1
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

        completion = (solved / total * 100) if total > 0 else 0

        print("\n===== Progress Statistics =====")
        print("Total problems:", total)
        print("Solved:", solved)
        print("Unsolved:", unsolved)
        print("Completion:", round(completion, 1), "%")

        print("\n===== Difficulty Statistics =====")
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
        if len(problems) == 0:
            print("No problems available.")
        else:
            for i, problem in enumerate(problems, start=1):
                status = "Solved" if problem.get("solved", False) else "Not solved"
                print(i, ".", problem["name"], "-", status)

            number = input("Enter the problem number to mark as solved: ")

            if number.isdigit():
                number = int(number)

                if 1 <= number <= len(problems):
                    problems[number - 1]["solved"] = True

                    with open("problems.json", "w") as file:
                        json.dump(problems, file, indent=4)

                    print("Problem marked as solved!")
                else:
                    print("Invalid problem number.")
            else:
                print("Please enter a valid number.")
    elif choice == "5":
        print("\n===== Search & Filter =====")
        print("1. Search by problem name")
        print("2. Filter by topic")
        print("3. Filter by difficulty")
        print("4. Back to main menu")

        filter_choice = input("Choose an option: ")

        if filter_choice == "4":
            continue
        elif filter_choice not in ["1", "2", "3"]:
            print("Invalid choice.")
        elif len(problems) == 0:
            print("No problems recorded yet.")
        else:
            results = []

            if filter_choice == "1":
                search_name = input("Enter problem name: ").strip().lower()

                for problem in problems:
                    if search_name in problem["name"].lower():
                        results.append(problem)

            elif filter_choice == "2":
                search_topic = input("Enter topic: ").strip().lower()

                for problem in problems:
                    if search_topic == problem["topic"].strip().lower():
                        results.append(problem)

            elif filter_choice == "3":
                search_difficulty = input("Enter difficulty (Easy/Medium/Hard): ").strip().capitalize()

                if search_difficulty not in ["Easy", "Medium", "Hard"]:
                    print("Invalid difficulty.")
                    continue

                for problem in problems:
                    if problem["difficulty"] == search_difficulty:
                        results.append(problem)

            if results:
                print("\n===== Search Results =====")

                for problem in results:
                    status = "Solved" if problem.get("solved", False) else "Not solved"
                    print("\nProblem:", problem["name"])
                    print("Platform:", problem["platform"])
                    print("Topic:", problem["topic"])
                    print("Difficulty:", problem["difficulty"])
                    print("Status:", status)
            else:
                print("No matching problems found.")
    elif choice == "6":
        print("Keep coding. Keep improving!")
        break

    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")
