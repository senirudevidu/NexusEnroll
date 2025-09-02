from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from backend.dal.user import Student
from backend.dal.enrollment import Enrollment


# Observer Interface
class NotificationObserver(ABC):
    """Abstract Observer interface for notification system"""
    
    @abstractmethod
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle notification when an event occurs"""
        pass
    
    @abstractmethod
    def get_observer_type(self) -> str:
        """Return the type of observer"""
        pass


# Subject Interface
class NotificationSubject(ABC):
    """Abstract Subject interface for notification system"""
    
    @abstractmethod
    def attach(self, observer: NotificationObserver) -> None:
        """Attach an observer to the subject"""
        pass
    
    @abstractmethod
    def detach(self, observer: NotificationObserver) -> None:
        """Detach an observer from the subject"""
        pass
    
    @abstractmethod
    def notify(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Notify all observers about an event"""
        pass


# Concrete Subject Implementation
class EnrollmentNotificationSubject(NotificationSubject):
    """Concrete Subject that manages enrollment-related notifications"""
    
    def __init__(self):
        self._observers: List[NotificationObserver] = []
        self._notification_log: List[Dict[str, Any]] = []
    
    def attach(self, observer: NotificationObserver) -> None:
        """Attach an observer to receive notifications"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"🔔 {observer.get_observer_type()} observer attached to notification system")
    
    def detach(self, observer: NotificationObserver) -> None:
        """Detach an observer from receiving notifications"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"🔕 {observer.get_observer_type()} observer detached from notification system")
    
    def notify(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Notify all attached observers about an enrollment event"""
        timestamp = datetime.now()
        
        # Log the notification
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'event_data': event_data,
            'observers_notified': len(self._observers)
        }
        self._notification_log.append(log_entry)
        
        print(f"\n📢 NOTIFICATION EVENT: {event_type} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Event Data: {event_data}")
        print(f"Notifying {len(self._observers)} observers...")
        
        # Notify all observers
        for observer in self._observers:
            try:
                observer.update(event_type, event_data)
            except Exception as e:
                print(f"❌ Error notifying {observer.get_observer_type()}: {str(e)}")
    
    def get_notification_log(self) -> List[Dict[str, Any]]:
        """Get the complete notification log"""
        return self._notification_log.copy()
    
    def get_observers_count(self) -> int:
        """Get the number of attached observers"""
        return len(self._observers)


# Concrete Observer Implementations

class StudentObserver(NotificationObserver):
    """Observer for student-related notifications (waitlist, enrollment updates)"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.student_dal = Student(db_connection)
        self.enrollment_dal = Enrollment(db_connection)
    
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle student notifications"""
        if event_type == "COURSE_DROPPED":
            self._notify_waitlisted_students(event_data)
        elif event_type == "ENROLLMENT_SUCCESSFUL":
            self._notify_student_enrollment_success(event_data)
        elif event_type == "ENROLLMENT_FAILED":
            self._notify_student_enrollment_failure(event_data)
        elif event_type == "COURSE_CAPACITY_UPDATED":
            self._notify_course_availability_change(event_data)
    
    def _notify_waitlisted_students(self, event_data: Dict[str, Any]) -> None:
        """Notify students on waitlist when a spot opens up"""
        course_id = event_data.get('course_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        dropped_student_id = event_data.get('student_id')
        
        print(f"📚 StudentObserver: Checking waitlist for course {course_name} (ID: {course_id})")
        
        # Simulate getting waitlisted students (in a real system, this would be from a waitlist table)
        waitlisted_students = self._get_waitlisted_students(course_id)
        
        for student in waitlisted_students:
            student_id, student_name, student_email = student
            if student_id != dropped_student_id:  # Don't notify the student who dropped
                self._send_notification_to_student(
                    student_id, 
                    student_name, 
                    student_email,
                    f"🎉 Great news! A spot has opened up in {course_name}. You can now enroll!",
                    "WAITLIST_SPOT_AVAILABLE"
                )
    
    def _notify_student_enrollment_success(self, event_data: Dict[str, Any]) -> None:
        """Notify student of successful enrollment"""
        student_id = event_data.get('student_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        
        student_info = self._get_student_info(student_id)
        if student_info:
            student_name, student_email = student_info
            self._send_notification_to_student(
                student_id,
                student_name,
                student_email,
                f"✅ Successfully enrolled in {course_name}. Welcome to the class!",
                "ENROLLMENT_CONFIRMATION"
            )
    
    def _notify_student_enrollment_failure(self, event_data: Dict[str, Any]) -> None:
        """Notify student of enrollment failure"""
        student_id = event_data.get('student_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        reason = event_data.get('reason', 'Unknown reason')
        
        student_info = self._get_student_info(student_id)
        if student_info:
            student_name, student_email = student_info
            self._send_notification_to_student(
                student_id,
                student_name,
                student_email,
                f"❌ Enrollment in {course_name} failed: {reason}",
                "ENROLLMENT_FAILURE"
            )
    
    def _notify_course_availability_change(self, event_data: Dict[str, Any]) -> None:
        """Notify about course availability changes"""
        course_id = event_data.get('course_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        available_seats = event_data.get('available_seats', 0)
        
        if available_seats > 0:
            waitlisted_students = self._get_waitlisted_students(course_id)[:available_seats]
            for student in waitlisted_students:
                student_id, student_name, student_email = student
                self._send_notification_to_student(
                    student_id,
                    student_name,
                    student_email,
                    f"🎯 {course_name} now has {available_seats} available seat(s). Enroll now!",
                    "COURSE_AVAILABLE"
                )
    
    def _get_waitlisted_students(self, course_id: int) -> List[tuple]:
        """Get students on waitlist for a course (simulated)"""
        # In a real system, this would query a waitlist table
        # For simulation, we'll return some mock waitlisted students
        return [
            (101, "Alice Johnson", "alice.johnson@university.edu"),
            (102, "Bob Smith", "bob.smith@university.edu"),
            (103, "Carol Davis", "carol.davis@university.edu")
        ]
    
    def _get_student_info(self, student_id: int) -> tuple:
        """Get student information"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT firstName, lastName, email 
            FROM Users 
            WHERE user_id = %s AND userType = 'Student'
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                first_name, last_name, email = result
                return f"{first_name} {last_name}", email
            return None
            
        except Exception as e:
            print(f"Error getting student info: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    def _send_notification_to_student(self, student_id: int, student_name: str, 
                                     student_email: str, message: str, notification_type: str) -> None:
        """Send notification to a student (simulated email)"""
        print(f"📧 EMAIL TO STUDENT:")
        print(f"   To: {student_name} ({student_email})")
        print(f"   Subject: Course Enrollment Update")
        print(f"   Message: {message}")
        print(f"   Type: {notification_type}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
    
    def get_observer_type(self) -> str:
        return "Student Observer"


class AdvisorObserver(NotificationObserver):
    """Observer for advisor-related notifications"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle advisor notifications"""
        if event_type == "COURSE_DROPPED":
            self._notify_advisor_about_drop(event_data)
        elif event_type == "ENROLLMENT_SUCCESSFUL":
            self._notify_advisor_about_enrollment(event_data)
        elif event_type == "CRITICAL_COURSE_DROPPED":
            self._notify_advisor_critical_course_drop(event_data)
    
    def _notify_advisor_about_drop(self, event_data: Dict[str, Any]) -> None:
        """Notify advisor when their advisee drops a course"""
        student_id = event_data.get('student_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        course_id = event_data.get('course_id')
        
        # Get student's advisor
        advisor_info = self._get_student_advisor(student_id)
        if advisor_info:
            advisor_id, advisor_name, advisor_email = advisor_info
            student_info = self._get_student_info(student_id)
            
            if student_info:
                student_name, student_email = student_info
                
                # Check if this is a critical course (core requirement)
                is_critical = self._is_critical_course(course_id, student_id)
                
                message = f"📋 Your advisee {student_name} has dropped {course_name}."
                if is_critical:
                    message += " ⚠️ This is a critical course for their degree program."
                
                self._send_notification_to_advisor(
                    advisor_id, advisor_name, advisor_email, message, 
                    "ADVISEE_COURSE_DROP", student_name
                )
    
    def _notify_advisor_about_enrollment(self, event_data: Dict[str, Any]) -> None:
        """Notify advisor when their advisee successfully enrolls"""
        student_id = event_data.get('student_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        
        advisor_info = self._get_student_advisor(student_id)
        if advisor_info:
            advisor_id, advisor_name, advisor_email = advisor_info
            student_info = self._get_student_info(student_id)
            
            if student_info:
                student_name, student_email = student_info
                message = f"✅ Your advisee {student_name} has successfully enrolled in {course_name}."
                
                self._send_notification_to_advisor(
                    advisor_id, advisor_name, advisor_email, message,
                    "ADVISEE_ENROLLMENT_SUCCESS", student_name
                )
    
    def _notify_advisor_critical_course_drop(self, event_data: Dict[str, Any]) -> None:
        """Notify advisor about critical course drops requiring immediate attention"""
        student_id = event_data.get('student_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        
        advisor_info = self._get_student_advisor(student_id)
        if advisor_info:
            advisor_id, advisor_name, advisor_email = advisor_info
            student_info = self._get_student_info(student_id)
            
            if student_info:
                student_name, student_email = student_info
                message = (f"🚨 URGENT: Your advisee {student_name} has dropped {course_name}, "
                          f"which is a critical course for their degree. Please schedule a meeting immediately.")
                
                self._send_notification_to_advisor(
                    advisor_id, advisor_name, advisor_email, message,
                    "CRITICAL_COURSE_DROP_ALERT", student_name
                )
    
    def _get_student_advisor(self, student_id: int) -> tuple:
        """Get advisor information for a student"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            # Simulated advisor assignment (in real system, would be in database)
            # For demo, we'll assign advisor based on student ID modulo
            advisor_assignments = {
                1: (201, "Dr. Sarah Wilson", "sarah.wilson@university.edu"),
                2: (202, "Dr. Michael Brown", "michael.brown@university.edu"),
                3: (203, "Dr. Emily Chen", "emily.chen@university.edu")
            }
            
            # Simple assignment logic for demo
            advisor_key = (student_id % 3) + 1
            return advisor_assignments.get(advisor_key)
            
        except Exception as e:
            print(f"Error getting advisor info: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    def _get_student_info(self, student_id: int) -> tuple:
        """Get student information"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT firstName, lastName, email 
            FROM Users 
            WHERE user_id = %s AND userType = 'Student'
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                first_name, last_name, email = result
                return f"{first_name} {last_name}", email
            return None
            
        except Exception as e:
            print(f"Error getting student info: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    def _is_critical_course(self, course_id: int, student_id: int) -> bool:
        """Check if a course is critical for the student's degree"""
        # Simulated logic - in real system, would check degree requirements
        critical_courses = [1, 2, 3, 5, 8]  # Example critical course IDs
        return course_id in critical_courses
    
    def _send_notification_to_advisor(self, advisor_id: int, advisor_name: str, 
                                     advisor_email: str, message: str, 
                                     notification_type: str, student_name: str) -> None:
        """Send notification to an advisor (simulated email)"""
        print(f"📧 EMAIL TO ADVISOR:")
        print(f"   To: {advisor_name} ({advisor_email})")
        print(f"   Subject: Advisee Update - {student_name}")
        print(f"   Message: {message}")
        print(f"   Type: {notification_type}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
    
    def get_observer_type(self) -> str:
        return "Advisor Observer"


class AdminObserver(NotificationObserver):
    """Observer for administrator-related notifications"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def update(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle administrator notifications"""
        if event_type in ["COURSE_DROPPED", "ENROLLMENT_SUCCESSFUL"]:
            self._notify_enrollment_statistics(event_data)
        elif event_type == "SYSTEM_ERROR":
            self._notify_system_error(event_data)
        elif event_type == "CAPACITY_WARNING":
            self._notify_capacity_warning(event_data)
        elif event_type == "HIGH_DROP_RATE":
            self._notify_high_drop_rate(event_data)
    
    def _notify_enrollment_statistics(self, event_data: Dict[str, Any]) -> None:
        """Notify admins about enrollment statistics updates"""
        course_id = event_data.get('course_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        event_type = event_data.get('event_type', 'Unknown')
        
        # Get current enrollment statistics
        stats = self._get_course_statistics(course_id)
        if stats:
            enrolled_count, capacity, available_seats = stats
            utilization = (enrolled_count / capacity) * 100 if capacity > 0 else 0
            
            message = (f"📊 Course Statistics Update for {course_name}:\n"
                      f"   Enrolled: {enrolled_count}/{capacity} ({utilization:.1f}% utilization)\n"
                      f"   Available Seats: {available_seats}\n"
                      f"   Event: {event_type}")
            
            # Alert if utilization is very high or very low
            if utilization > 95:
                message += "\n⚠️ Course nearly full - consider adding more sections"
            elif utilization < 30 and enrolled_count > 0:
                message += "\n📉 Low enrollment - consider promotional activities"
            
            self._send_notification_to_admins(message, "ENROLLMENT_STATISTICS")
    
    def _notify_system_error(self, event_data: Dict[str, Any]) -> None:
        """Notify admins about system errors"""
        error_type = event_data.get('error_type', 'Unknown Error')
        error_message = event_data.get('error_message', 'No details available')
        affected_component = event_data.get('component', 'Unknown Component')
        
        message = (f"🚨 SYSTEM ERROR ALERT:\n"
                  f"   Component: {affected_component}\n"
                  f"   Error Type: {error_type}\n"
                  f"   Details: {error_message}\n"
                  f"   Immediate attention required!")
        
        self._send_notification_to_admins(message, "SYSTEM_ERROR", urgent=True)
    
    def _notify_capacity_warning(self, event_data: Dict[str, Any]) -> None:
        """Notify admins about course capacity warnings"""
        course_id = event_data.get('course_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        available_seats = event_data.get('available_seats', 0)
        capacity = event_data.get('capacity', 0)
        
        if available_seats <= 2 and capacity > 0:
            message = (f"⚠️ CAPACITY WARNING: {course_name} is almost full!\n"
                      f"   Only {available_seats} seats remaining out of {capacity}\n"
                      f"   Consider opening additional sections or waitlist management")
            
            self._send_notification_to_admins(message, "CAPACITY_WARNING")
    
    def _notify_high_drop_rate(self, event_data: Dict[str, Any]) -> None:
        """Notify admins about unusually high drop rates"""
        course_id = event_data.get('course_id')
        course_name = event_data.get('course_name', 'Unknown Course')
        drop_count = event_data.get('drop_count', 0)
        total_enrolled = event_data.get('total_enrolled', 0)
        
        if total_enrolled > 0:
            drop_rate = (drop_count / total_enrolled) * 100
            if drop_rate > 20:  # Alert if drop rate exceeds 20%
                message = (f"📉 HIGH DROP RATE ALERT: {course_name}\n"
                          f"   Drop Rate: {drop_rate:.1f}% ({drop_count}/{total_enrolled})\n"
                          f"   Investigate potential issues with course content or delivery")
                
                self._send_notification_to_admins(message, "HIGH_DROP_RATE")
    
    def _get_course_statistics(self, course_id: int) -> tuple:
        """Get current course enrollment statistics"""
        try:
            conn = self.db.get_db_connection()
            cursor = conn.cursor()
            
            query = """
            SELECT 
                COUNT(e.enrollment_id) as enrolled_count,
                c.capacity,
                c.availableSeats
            FROM Course c
            LEFT JOIN Enrollment e ON c.course_id = e.course_id AND e.enrollmentStatus = 'Active'
            WHERE c.course_id = %s
            GROUP BY c.course_id, c.capacity, c.availableSeats
            """
            cursor.execute(query, (course_id,))
            result = cursor.fetchone()
            
            return result if result else None
            
        except Exception as e:
            print(f"Error getting course statistics: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    
    def _send_notification_to_admins(self, message: str, notification_type: str, urgent: bool = False) -> None:
        """Send notification to administrators (simulated email/dashboard alert)"""
        admin_list = [
            "admin@university.edu",
            "registrar@university.edu",
            "dean@university.edu"
        ]
        
        priority = "🚨 URGENT" if urgent else "📋 INFO"
        
        print(f"📧 ADMIN NOTIFICATION ({priority}):")
        print(f"   To: {', '.join(admin_list)}")
        print(f"   Subject: Enrollment System Alert - {notification_type}")
        print(f"   Message: {message}")
        print(f"   Type: {notification_type}")
        print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if urgent:
            print(f"   🔔 SMS alerts also sent to on-call administrators")
        print("-" * 50)
    
    def get_observer_type(self) -> str:
        return "Admin Observer"


# Notification Manager - Facade for the entire notification system
class NotificationManager:
    """Manages the entire notification system"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.subject = EnrollmentNotificationSubject()
        
        # Initialize and attach observers
        self.student_observer = StudentObserver(db_connection)
        self.advisor_observer = AdvisorObserver(db_connection)
        self.admin_observer = AdminObserver(db_connection)
        
        # Attach all observers by default
        self.attach_all_observers()
    
    def attach_all_observers(self) -> None:
        """Attach all observers to the notification system"""
        self.subject.attach(self.student_observer)
        self.subject.attach(self.advisor_observer)
        self.subject.attach(self.admin_observer)
    
    def detach_observer(self, observer_type: str) -> None:
        """Detach a specific observer type"""
        observer_map = {
            'student': self.student_observer,
            'advisor': self.advisor_observer,
            'admin': self.admin_observer
        }
        
        observer = observer_map.get(observer_type.lower())
        if observer:
            self.subject.detach(observer)
    
    def attach_observer(self, observer_type: str) -> None:
        """Attach a specific observer type"""
        observer_map = {
            'student': self.student_observer,
            'advisor': self.advisor_observer,
            'admin': self.admin_observer
        }
        
        observer = observer_map.get(observer_type.lower())
        if observer:
            self.subject.attach(observer)
    
    def notify_course_dropped(self, student_id: int, course_id: int, course_name: str) -> None:
        """Notify about a course drop event"""
        event_data = {
            'student_id': student_id,
            'course_id': course_id,
            'course_name': course_name,
            'timestamp': datetime.now(),
            'event_type': 'COURSE_DROPPED'
        }
        self.subject.notify("COURSE_DROPPED", event_data)
    
    def notify_enrollment_successful(self, student_id: int, course_id: int, course_name: str) -> None:
        """Notify about successful enrollment"""
        event_data = {
            'student_id': student_id,
            'course_id': course_id,
            'course_name': course_name,
            'timestamp': datetime.now(),
            'event_type': 'ENROLLMENT_SUCCESSFUL'
        }
        self.subject.notify("ENROLLMENT_SUCCESSFUL", event_data)
    
    def notify_enrollment_failed(self, student_id: int, course_id: int, course_name: str, reason: str) -> None:
        """Notify about enrollment failure"""
        event_data = {
            'student_id': student_id,
            'course_id': course_id,
            'course_name': course_name,
            'reason': reason,
            'timestamp': datetime.now(),
            'event_type': 'ENROLLMENT_FAILED'
        }
        self.subject.notify("ENROLLMENT_FAILED", event_data)
    
    def notify_system_error(self, error_type: str, error_message: str, component: str) -> None:
        """Notify about system errors"""
        event_data = {
            'error_type': error_type,
            'error_message': error_message,
            'component': component,
            'timestamp': datetime.now()
        }
        self.subject.notify("SYSTEM_ERROR", event_data)
    
    def notify_capacity_warning(self, course_id: int, course_name: str, available_seats: int, capacity: int) -> None:
        """Notify about course capacity warnings"""
        event_data = {
            'course_id': course_id,
            'course_name': course_name,
            'available_seats': available_seats,
            'capacity': capacity,
            'timestamp': datetime.now()
        }
        self.subject.notify("CAPACITY_WARNING", event_data)
    
    def get_notification_statistics(self) -> Dict[str, Any]:
        """Get notification system statistics"""
        return {
            'observers_count': self.subject.get_observers_count(),
            'total_notifications': len(self.subject.get_notification_log()),
            'notification_log': self.subject.get_notification_log()[-10:],  # Last 10 notifications
            'observers': [
                self.student_observer.get_observer_type(),
                self.advisor_observer.get_observer_type(),
                self.admin_observer.get_observer_type()
            ]
        }
    
    def demo_notification_system(self) -> None:
        """Demonstrate the notification system with sample events"""
        print("\n" + "="*60)
        print("🎯 NOTIFICATION SYSTEM DEMO")
        print("="*60)
        
        # Demo 1: Student drops a course
        print("\n🎬 DEMO 1: Student drops a course")
        self.notify_course_dropped(1, 5, "Advanced Database Systems")
        
        # Demo 2: Successful enrollment
        print("\n🎬 DEMO 2: Successful enrollment")
        self.notify_enrollment_successful(2, 3, "Web Development")
        
        # Demo 3: System error
        print("\n🎬 DEMO 3: System error occurs")
        self.notify_system_error("Database Connection", "Connection timeout to main database", "Enrollment Service")
        
        # Demo 4: Capacity warning
        print("\n🎬 DEMO 4: Course capacity warning")
        self.notify_capacity_warning(7, "Machine Learning", 1, 30)
        
        # Demo 5: Failed enrollment
        print("\n🎬 DEMO 5: Failed enrollment")
        self.notify_enrollment_failed(3, 8, "Advanced Mathematics", "Prerequisites not met")
        
        print("\n" + "="*60)
        print("📊 NOTIFICATION SYSTEM STATISTICS")
        print("="*60)
        stats = self.get_notification_statistics()
        print(f"Active Observers: {stats['observers_count']}")
        print(f"Total Notifications Sent: {stats['total_notifications']}")
        print(f"Observer Types: {', '.join(stats['observers'])}")
