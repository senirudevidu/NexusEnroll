from backend.dal.enrollment import Enrollment


class RosterService:
    def __init__(self, db):
        self.db = db
        self.enrollment = Enrollment(self.db)

    def get_class_roster(self, faculty_id, course_id):
        """Get class roster for a specific course"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            result = self.enrollment.get_class_roster(cursor, faculty_id, course_id)
            
            if result["status"] == "Success":
                # Format the response according to requirements
                response = {
                    "status": "Success",
                    "course": result["course_info"]["course_name"],
                    "instructor": result["course_info"]["instructor"],
                    "students": []
                }
                
                if result["students"]:
                    for student in result["students"]:
                        student_data = {
                            "id": student[1],  # student_id
                            "name": f"{student[2]} {student[3]}",  # firstName lastName
                            "email": student[4],  # email
                            "phone": student[5] if student[5] else "N/A",  # mobileNo
                            "enrollment_status": student[6],  # enrollmentStatus
                            "mark_status": student[7]  # markStatus
                        }
                        response["students"].append(student_data)
                else:
                    response["message"] = "No students enrolled yet"
                
                return response
            else:
                return result
                
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def get_faculty_courses(self, faculty_id):
        """Get all courses taught by a faculty member"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()

        try:
            courses = self.enrollment.get_faculty_courses(cursor, faculty_id)
            
            formatted_courses = []
            for course in courses:
                course_data = {
                    "course_id": course[0],
                    "course_name": course[1],
                    "description": course[2],
                    "capacity": course[3],
                    "available_seats": course[4],
                    "enrolled_count": course[5],
                    "department": course[6]
                }
                formatted_courses.append(course_data)
            
            return {"status": "Success", "courses": formatted_courses}
                
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def export_roster_csv(self, faculty_id, course_id):
        """Export roster to CSV format"""
        result = self.get_class_roster(faculty_id, course_id)
        
        if result["status"] == "Success" and result.get("students"):
            csv_content = "Student ID,Name,Email,Phone,Enrollment Status,Mark Status\n"
            for student in result["students"]:
                csv_content += f'{student["id"]},"{student["name"]}",{student["email"]},{student["phone"]},{student["enrollment_status"]},{student["mark_status"]}\n'
            
            return {
                "status": "Success",
                "content": csv_content,
                "filename": f'{result["course"].replace(" ", "_")}_roster.csv'
            }
        else:
            return {"status": "Error", "message": "No data to export"}
