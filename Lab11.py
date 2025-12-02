import os
import matplotlib.pyplot as plt



def load_students(path):
    students = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid = line[:3]
            name = line[3:].strip()
            students[name] = sid
    return students



def load_assignments(path):
    assignments = {}
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = lines[i + 1]
        pts = int(lines[i + 2])
        assignments[name] = {"id": aid, "points": pts}
    return assignments



def load_submissions(directory):
    submissions = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if not os.path.isfile(file_path):
            continue
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 3:
                    continue
                sid, aid, pct = parts
                sid = sid.strip()
                aid = aid.strip()
                pct = float(pct.strip()) / 100  
                if aid not in submissions:
                    submissions[aid] = {}
                submissions[aid][sid] = pct
    return submissions



def calculate_student_grade(student_name, students, assignments, submissions):
    if student_name not in students:
        print("Student not found")
        return
    sid = students[student_name]
    total_points = 0
    for aname, adata in assignments.items():
        aid = adata["id"]
        pts = adata["points"]
        percent = submissions[aid][sid]
        total_points += percent * pts
    final_grade = round((total_points / 1000) * 100)
    print(f"{final_grade}%")



def assignment_stats(aname, assignments, submissions):
    if aname not in assignments:
        print("Assignment not found")
        return
    aid = assignments[aname]["id"]
    scores = [pct * 100 for pct in submissions[aid].values()]
    print(f"Min: {int(min(scores))}%")
    print(f"Avg: {int(sum(scores) / len(scores))}%")
    print(f"Max: {int(max(scores))}%")



def assignment_graph(aname, assignments, submissions):
    if aname not in assignments:
        print("Assignment not found")
        return
    aid = assignments[aname]["id"]
    scores = [pct * 100 for pct in submissions[aid].values()]
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(aname)
    plt.xlabel("Score (%)")
    plt.ylabel("Count")
    plt.show()


def main():
    students = load_students("data/students.txt")
    assignments = load_assignments("data/assignments.txt")
    submissions = load_submissions("data/submissions")

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")

    selection = input("Enter your selection: ")

    if selection == "1":
        name = input("What is the student's name: ")
        calculate_student_grade(name, students, assignments, submissions)
    elif selection == "2":
        aname = input("What is the assignment name: ")
        assignment_stats(aname, assignments, submissions)
    elif selection == "3":
        aname = input("What is the assignment name: ")
        assignment_graph(aname, assignments, submissions)


if __name__ == "__main__":
    main()
