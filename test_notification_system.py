"""
Test and Demo for Notification System
Demonstrates the Observer Design Pattern implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.service.notificationService import (
    NotificationManager, 
    StudentObserver, 
    AdvisorObserver, 
    AdminObserver,
    EnrollmentNotificationSubject
)
from backend.dal.dbconfig import dbconfig


def test_individual_observers():
    """Test individual observer functionality"""
    print("\n" + "="*60)
    print("🧪 TESTING INDIVIDUAL OBSERVERS")
    print("="*60)
    
    # Mock database connection
    db = dbconfig()
    
    # Test Student Observer
    print("\n📚 Testing Student Observer...")
    student_obs = StudentObserver(db)
    test_event_data = {
        'student_id': 1,
        'course_id': 5,
        'course_name': 'Advanced Database Systems'
    }
    student_obs.update("COURSE_DROPPED", test_event_data)
    
    # Test Advisor Observer
    print("\n👨‍🏫 Testing Advisor Observer...")
    advisor_obs = AdvisorObserver(db)
    advisor_obs.update("COURSE_DROPPED", test_event_data)
    
    # Test Admin Observer
    print("\n🏛️ Testing Admin Observer...")
    admin_obs = AdminObserver(db)
    admin_obs.update("COURSE_DROPPED", test_event_data)


def test_observer_attach_detach():
    """Test observer attachment and detachment"""
    print("\n" + "="*60)
    print("🔗 TESTING OBSERVER ATTACHMENT/DETACHMENT")
    print("="*60)
    
    # Create subject
    subject = EnrollmentNotificationSubject()
    db = dbconfig()
    
    # Create observers
    student_obs = StudentObserver(db)
    advisor_obs = AdvisorObserver(db)
    admin_obs = AdminObserver(db)
    
    print(f"Initial observers: {subject.get_observers_count()}")
    
    # Attach observers
    subject.attach(student_obs)
    subject.attach(advisor_obs)
    subject.attach(admin_obs)
    
    print(f"After attaching 3 observers: {subject.get_observers_count()}")
    
    # Try to attach same observer again (should not duplicate)
    subject.attach(student_obs)
    print(f"After trying to attach duplicate: {subject.get_observers_count()}")
    
    # Detach an observer
    subject.detach(advisor_obs)
    print(f"After detaching advisor: {subject.get_observers_count()}")
    
    # Test notification with remaining observers
    test_event = {
        'student_id': 1,
        'course_id': 3,
        'course_name': 'Software Engineering'
    }
    subject.notify("ENROLLMENT_SUCCESSFUL", test_event)


def test_notification_manager():
    """Test the complete notification manager"""
    print("\n" + "="*60)
    print("🎯 TESTING NOTIFICATION MANAGER")
    print("="*60)
    
    db = dbconfig()
    manager = NotificationManager(db)
    
    # Run the built-in demo
    manager.demo_notification_system()
    
    # Test observer management
    print("\n🔧 Testing observer management...")
    initial_count = manager.subject.get_observers_count()
    print(f"Initial observer count: {initial_count}")
    
    # Detach student observer
    manager.detach_observer('student')
    print(f"After detaching student observer: {manager.subject.get_observers_count()}")
    
    # Re-attach student observer
    manager.attach_observer('student')
    print(f"After re-attaching student observer: {manager.subject.get_observers_count()}")
    
    # Get statistics
    stats = manager.get_notification_statistics()
    print(f"\nFinal statistics:")
    print(f"- Active observers: {stats['observers_count']}")
    print(f"- Total notifications: {stats['total_notifications']}")


def test_error_handling():
    """Test error handling in the notification system"""
    print("\n" + "="*60)
    print("⚠️ TESTING ERROR HANDLING")
    print("="*60)
    
    db = dbconfig()
    manager = NotificationManager(db)
    
    # Test with invalid data
    try:
        manager.notify_enrollment_failed(
            None, None, "Invalid Course", "Invalid data test"
        )
        print("✅ System handled invalid data gracefully")
    except Exception as e:
        print(f"❌ Error handling failed: {e}")
    
    # Test system error notification
    manager.notify_system_error(
        "Test Error", 
        "This is a simulated error for testing", 
        "Test Component"
    )


def demo_real_world_scenario():
    """Demonstrate a real-world enrollment scenario"""
    print("\n" + "="*80)
    print("🌍 REAL-WORLD SCENARIO DEMONSTRATION")
    print("="*80)
    print("Scenario: Peak enrollment period with multiple events happening")
    
    db = dbconfig()
    manager = NotificationManager(db)
    
    # Scenario: Multiple students trying to enroll in popular courses
    print("\n📅 Monday 8:00 AM - Enrollment opens for CS courses")
    
    # High demand course fills up quickly
    manager.notify_enrollment_successful(101, 15, "Machine Learning")
    manager.notify_enrollment_successful(102, 15, "Machine Learning")
    manager.notify_enrollment_successful(103, 15, "Machine Learning")
    
    # Course reaches capacity
    manager.notify_capacity_warning(15, "Machine Learning", 2, 30)
    
    # Some students can't get in
    manager.notify_enrollment_failed(104, 15, "Machine Learning", "Course is full")
    manager.notify_enrollment_failed(105, 15, "Machine Learning", "Course is full")
    
    print("\n📅 Tuesday 10:30 AM - A student drops the popular course")
    manager.notify_course_dropped(102, 15, "Machine Learning")
    
    print("\n📅 Tuesday 2:15 PM - System experiences issues")
    manager.notify_system_error(
        "Database Timeout", 
        "High load causing database connection timeouts", 
        "Enrollment Service"
    )
    
    print("\n📅 Wednesday 9:00 AM - Students adjust their schedules")
    manager.notify_course_dropped(103, 8, "Advanced Calculus")  # Critical course
    manager.notify_enrollment_successful(106, 12, "Web Development")
    
    # Final statistics
    print("\n📊 FINAL SCENARIO STATISTICS:")
    stats = manager.get_notification_statistics()
    print(f"Total notifications processed: {stats['total_notifications']}")
    print(f"Active observers: {stats['observers_count']}")
    print(f"System handled {stats['total_notifications']} events seamlessly!")


def main():
    """Run all tests and demonstrations"""
    print("🚀 NEXUSENROLL NOTIFICATION SYSTEM TESTING")
    print("Implementing Observer Design Pattern")
    print("="*80)
    
    try:
        # Run individual tests
        test_individual_observers()
        test_observer_attach_detach()
        test_notification_manager()
        test_error_handling()
        
        # Run real-world scenario
        demo_real_world_scenario()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The Observer Design Pattern has been successfully implemented")
        print("with proper decoupling and extensibility.")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
