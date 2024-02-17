import pymongo

class StudentDatabase:
    def __init__(self, database_name, collection_name):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]
        self.student_id_counter = self.collection.count_documents({}) + 1

    def add_student(self, name, age, **kwargs):
        student = {
            "student_id": self.student_id_counter,
            "name": name,
            "age" : age
        }
        for key, value in kwargs.items():
            student[key] = value
        self.collection.insert_one(student)
        self.student_id_counter += 1
        print("Student record added successfully.")

    def remove_student(self, student_id):
        result = self.collection.delete_one({"student_id": student_id})
        if result.deleted_count > 0:
            print("Student  deleted successfully.")
        else:
            print("Student  not found.")

    def search_student(self, student_id):
        student = self.collection.find_one({"student_id": student_id})
        if student:
            print("Student  found:")
            print(f"ID: {student['student_id']} , Name: {student['name']} ,  Age: {student['age']} ")
        else:
            print("Student  not found.")

    def display_students(self):
        students = self.collection.find()
        if students:
            print("Students :")
            for student in students:
                print(f"ID: {student['student_id']} , Name: {student['name']} ,  Age: {student['age']} ")
        else:
            print("No students  found.")

    def edit_student(self, student_id):
        student = self.collection.find_one({"student_id": student_id})
        if student:
            print("Current student :")
            print(student)

            name = input("Enter new name (leave blank to keep current value): ")
            age  = input("Enter new age (leave blank to keep current value): ")

            updated_student = {}
            if name:
                updated_student["name"] = name
            if age:
                updated_student["age"] = age

            if updated_student:
                self.collection.update_one({"student_id": student_id}, {"$set": updated_student})
                print("Student record updated successfully.")
            else:
                print("No changes made to the student record.")
        else:
            print("Student record not found.")

def main():
    database = StudentDatabase("student_records", "students")

    while True:
        print("\nStudent Records Management System")
        print("1. Add Student Record")
        print("2. Remove Student Record")
        print("3. Search for Student Record")
        print("4. Display Student Details")
        print("5. Edit Student Record")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            name = input("Enter student name: ")
            age = input("Enter student age: ")
            database.add_student(name, age)

        elif choice == "2":
            student_id = int(input("Enter student ID to be removed: "))
            database.remove_student(student_id)

        elif choice == "3":
            student_id = int(input("Enter student ID to search: "))
            database.search_student(student_id)

        elif choice == "4":
            database.display_students()

        elif choice == "5":
            student_id = int(input("Enter student ID to edit: "))
            database.edit_student(student_id)

        elif choice == "6":
            print("Exiting the program.")
            database.client.close()
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()