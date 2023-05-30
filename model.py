from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User
from pyclbr import Class
import datetime
from django.db import models

# Model for storing inventory
class Inventory(models.Model):
    ITEM_TYPES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('meat', 'Meat'),
        ('poultry', 'Poultry'),
        ('dairy_products', 'Dairy Products'),
        ('grains', 'Grains'),
        ('cereals', 'Cereals'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('baked_goods', 'Baked Goods'),
        ('stationery', 'Stationery'),
        ('textbooks', 'Textbooks'),
        ('exercise_books', 'Exercise Books'),
        ('art_supplies', 'Art Supplies'),
        ('cleaning_supplies', 'Cleaning Supplies'),
        ('toiletries', 'Toiletries'),
        ('bedding', 'Bedding'),
        ('uniforms', 'Uniforms'),
        ('sports_equipment', 'Sports Equipment'),
        ('playground_equipment', 'Playground Equipment'),
        ('teaching_aids', 'Teaching Aids'),
    ]

    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()  # Add the max_quantity field
    supply_datetime = models.DateTimeField()
    teachers = models.ManyToManyField('Teacher', through='InventoryTeacher')
    students = models.ManyToManyField('Student', through='InventoryStudent')
    workers = models.ManyToManyField('Worker', through='InventoryWorker')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='inventories', null=True, blank=True)

    def __str__(self):
        return self.item_name

    def get_deficit_color(self):
        deficit_percentage = (100 - (self.quantity * 100 / self.max_quantity))

        if deficit_percentage >= 95:
            return 'green'
        elif deficit_percentage >= 75:
            return 'purple'
        elif deficit_percentage >= 50:
            return 'yellow'
        else:
            return 'red'

# Model for storing teacher's inventory transactions
class InventoryTeacher(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    quantity_taken = models.PositiveIntegerField()
    transaction_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.inventory.item_name} taken by {self.teacher.name}"

# Model for storing student's inventory transactions
class InventoryStudent(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    quantity_taken = models.PositiveIntegerField()
    transaction_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.inventory.item_name} taken by {self.student.name}"

# Model for storing worker's inventory transactions
class InventoryWorker(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    quantity_taken = models.PositiveIntegerField()
    transaction_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.inventory.item_name} taken by {self.worker.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Create subjects for Junior Primary School
Subject.objects.create(name="Mathematics")
Subject.objects.create(name="English Language")
Subject.objects.create(name="Kiswahili Language")
Subject.objects.create(name="Environmental Studies/Science")
Subject.objects.create(name="Social Studies")
Subject.objects.create(name="Art and Craft")
Subject.objects.create(name="Music")
Subject.objects.create(name="Physical Education")

# Create subjects for Senior Primary School
Subject.objects.create(name="Mathematics")
Subject.objects.create(name="English Language")
Subject.objects.create(name="Kiswahili Language")
Subject.objects.create(name="Science")
Subject.objects.create(name="Social Studies")
Subject.objects.create(name="Religious Education")
Subject.objects.create(name="Art and Craft")
Subject.objects.create(name="Music")
Subject.objects.create(name="Physical Education")
Subject.objects.create(name="Computer Studies/ICT")

class StudentClassInfo(models.Model):
    class_name = models.CharField(max_length=20)
    class_short_form = models.CharField(max_length=10)

    def __str__(self):
        return self.class_name


class StudentSectionInfo(models.Model):
    section_name = models.CharField(max_length=20)

    def __str__(self):
        return self.section_name


class StudentShiftInfo(models.Model):
    shift_name = models.CharField(max_length=100)

    def __str__(self):
        return self.shift_name

def upload_to_passport(instance, filename):
    now = datetime.datetime.now()
    path = 'student/passport_photos/{}/{}/{}/{}'.format(now.year, now.month, now.day, filename)
    return path
   
# Model for storing student details
class Student(models.Model):
    ADMISSION_TYPE_CHOICES = [
        ('day', 'Day School'),
        ('boarding', 'Boarding School'),
        ('daycare', 'Daycare'),
    ]

    GRADE_CHOICES = [
        ('kindergarten', 'Kindergarten'),
        ('junior_primary', 'Junior Primary School'),
        ('senior_primary', 'Senior Primary School'),
    ]

    admission_number = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    class_type = models.ForeignKey(StudentClassInfo, on_delete=models.CASCADE)
    class_field = models.CharField(max_length=50, choices=GRADE_CHOICES)
    schooling_type = models.CharField(max_length=10, choices=ADMISSION_TYPE_CHOICES)
    passport_photo = models.ImageField(upload_to=upload_to_passport)
    birth_certificate = models.FileField(upload_to='student/birth_certificates/', null=True, blank=True)
    acceptance_letter = models.FileField(upload_to='student/acceptance_letters/', null=True, blank=True)
    address = models.TextField(blank=True)
    subjects = models.ManyToManyField(Subject)
    academic_year = models.CharField(max_length=100)
    admission_date = models.DateField()
    gender_choice = (
        ("male", "Male"),
        ("female", "Female"),
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    section_type = models.ForeignKey(StudentSectionInfo, on_delete=models.CASCADE)
    shift_type = models.ForeignKey(StudentShiftInfo, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["admission_number", "class_type"]

    def __str__(self):
        return self.name
    
class AttendanceManager(models.Manager):
    def create_attendance(self, student_class, student_id):
        student_obj = Student.objects.get(
            class_type__class_short_form=student_class,
            admission_number=student_id
        )
        attendance_obj = Attendance.objects.create(student=student_obj, status=1)
        return attendance_obj


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)

    objects = AttendanceManager()

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return self.student.admission_number
    

def upload_to_fathers_passport(instance, filename):
    now = datetime.datetime.now()
    path = 'father/passport_photos/{}/{}/{}/{}'.format(now.year, now.month, now.day, filename)
    return path

def upload_to_mothers_passport(instance, filename):
    now = datetime.datetime.now()
    path = 'mother/passport_images/{}/{}/{}/{}'.format(now.year, now.month, now.day, filename)
    return path

class Parent(models.Model):
    STUDENT_RELATIONSHIP_CHOICES = [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('guardian', 'Guardian'),
    ]

    fathers_name = models.CharField(max_length=100)
    fathers_passport_photo = models.ImageField(upload_to=upload_to_fathers_passport)
    fathers_identity_card_number = models.CharField(max_length=20, validators=[MaxLengthValidator(20)], unique=True)
    fathers_phone_number = models.CharField(max_length=20, unique=True)
    mothers_name = models.CharField(max_length=100)
    mothers_passport_photo = models.ImageField(upload_to=upload_to_mothers_passport)
    mothers_identity_card_number = models.CharField(max_length=20, validators=[MaxLengthValidator(20)], unique=True)
    mothers_phone_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=20, choices=STUDENT_RELATIONSHIP_CHOICES)
    address = models.TextField(blank=True)
    fathers_identity_card_document = models.FileField(upload_to='parent/identity_card_documents/father/', null=True, blank=True)
    mothers_identity_card_document = models.FileField(upload_to='parent/identity_card_documents/mother/', null=True, blank=True)
    students = models.ManyToManyField(Student)

    def save(self, *args, **kwargs):
        self.mothers_nid = self.mothers_identity_card_number
        super().save(*args, **kwargs)



class TeacherDeptInfo(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name

class TeacherSubInfo(models.Model):
    sub_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_name

# Model for storing teacher details
class Teacher(models.Model):
    RANK_CHOICES = [
        ('head', 'Head Teacher'),
        ('senior', 'Senior Teacher'),
        ('regular', 'Regular Teacher'),
        ('deputy', 'Deputy Headteacher'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('not_applicable', 'Not Applicable'),
    ]

    name = models.CharField(max_length=100)
    tsc_number = models.CharField(max_length=20, primary_key=True)
    id_number = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    rank = models.CharField(max_length=20, choices=RANK_CHOICES)
    classes_taught = models.ManyToManyField(Student, through='StudentMark')
    passport_photo = models.ImageField(upload_to='teacher/passport_photos/')
    kcpe_qualification = models.FileField(upload_to='teacher/qualifications/kcpe/', null=True, blank=True)
    kcse_qualification = models.FileField(upload_to='teacher/qualifications/kcse/', null=True, blank=True)
    undergraduate_degree = models.FileField(upload_to='teacher/qualifications/undergraduate/', null=True, blank=True)
    masters_degree = models.FileField(upload_to='teacher/qualifications/masters/', null=True, blank=True)
    postgraduate_degree = models.FileField(upload_to='teacher/qualifications/postgraduate/', null=True, blank=True)
    work_contract = models.FileField(upload_to='teacher/contracts/', null=True, blank=True)
    address = models.TextField(blank=True)
    subjects_taught = models.ManyToManyField(Subject)
    passing_year = models.CharField(max_length=100)
    joining_date = models.DateField()
    dept_type = models.ForeignKey(TeacherDeptInfo, on_delete=models.CASCADE)
    sub_type = models.ForeignKey(TeacherSubInfo, on_delete=models.CASCADE)
    salary = models.IntegerField()
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)

    def __str__(self):
        return self.name

class SchemeOfWork(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schemes_of_work')

    def __str__(self):
        return f"Scheme of Work for {self.teacher}"

class Row(models.Model):
    scheme_of_work = models.ForeignKey(SchemeOfWork, on_delete=models.CASCADE, related_name='rows')
    listing_number = models.IntegerField()
    column_index = models.IntegerField()
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    activity = models.TextField()

    def __str__(self):
        return f"Row {self.listing_number}: {self.title}"

    class Meta:
        ordering = ['listing_number', 'column_index']

# Model for storing worker details
def upload_to_passport_photo(instance, filename):
    now = datetime.datetime.now()
    path = 'worker/passport_photos/{}/{}/{}/{}'.format(now.year, now.month, now.day, filename)
    return path

class Worker(models.Model):
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('cook', 'Cook'),
        ('security_guard', 'Security Guard'),
        ('cleaner', 'Cleaner'),
        ('accountant_bursar', 'Accountant/Bursar'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('not_applicable', 'Not Applicable'),
    ]

    name = models.CharField(max_length=100)
    worker_id = models.CharField(max_length=20, primary_key=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    passport_photo = models.ImageField(upload_to=upload_to_passport_photo)
    work_contract = models.FileField(upload_to='worker/contracts/')
    kcpe_document = models.FileField(upload_to='worker/documents/kcpe/')
    kcse_document = models.FileField(upload_to='worker/documents/kcse/')
    qualification_document = models.FileField(upload_to='worker/qualifications/')
    id_card_document = models.FileField(upload_to='worker/documents/id_card/')
    address = models.TextField(blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    identity_card_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name



# Model for storing supplier details
def upload_to_passport_photo(instance, filename):
    now = datetime.datetime.now()
    path = 'supplier/passport_photos/{}/{}/{}/{}'.format(now.year, now.month, now.day, filename)
    return path

class Supplier(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('every_three_months', 'Every Three Months'),
        ('on_demand', 'On Demand'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('not_applicable', 'Not Applicable'),
    ]

    name = models.CharField(max_length=100)
    supplier_id_card_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    supplied_item = models.CharField(max_length=100)
    passport_photo = models.ImageField(upload_to=upload_to_passport_photo)
    address = models.TextField()
    id_card_document = models.FileField(upload_to='supplier/documents/id_card/')
    signed_deal_document = models.FileField(upload_to='supplier/documents/signed_deal/')
    supply_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    last_supply_date = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)

    def __str__(self):
        return self.name

# Model for storing student marks
class StudentMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50)  # Changed to CharField
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)  # New field
    subject = models.CharField(max_length=50)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

# Model for storing leave requests
class LeaveRequest(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        if self.worker:
            return f"{self.worker.name} - {self.start_date}"
        elif self.teacher:
            return f"{self.teacher.name} - {self.start_date}"
        else:
            return "Leave Request"

# Model for storing sick leave requests
class SickLeaveRequest(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        if self.worker:
            return f"{self.worker.name} - {self.start_date}"
        elif self.teacher:
            return f"{self.teacher.name} - {self.start_date}"
        else:
            return "Sick Leave Request"

# Model for storing payment receipts
class PaymentReceipt(models.Model):
    PAYMENT_TYPES = [
        ('student_school_fees', 'Student School Fees'),
        ('worker_salary', 'Worker Salary'),
        ('teacher_salary', 'Teacher Salary'),
        ('supplier_item_supply', 'Supplier Item Supply'),
        ('student_trip_fee', 'Student Trip Fee'),
        ('student_bursary', 'Student Bursary'),
        ('school_development_grant', 'School Development Grant'),
        ('school_contributions', 'School Contributions'),
        ('activity_funds', 'Activity Funds'),
    ]

    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPES)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        if self.payment_type == 'student_school_fees':
            return f"Student School Fees - {self.student.name}"
        elif self.payment_type == 'worker_salary':
            return f"Worker Salary - {self.worker.name}"
        elif self.payment_type == 'teacher_salary':
            return f"Teacher Salary - {self.worker.name}"
        elif self.payment_type == 'supplier_item_supply':
            return f"Supplier Item Supply - {self.supplier.name}"
        elif self.payment_type == 'student_trip_fee':
            return f"Student Trip Fee - {self.student.name}"
        elif self.payment_type == 'student_bursary':
            return f"Student Bursary - {self.student.name}"
        elif self.payment_type == 'school_development_grant':
            return "School Development Grant"
        elif self.payment_type == 'school_contributions':
            return "School Contributions"
        elif self.payment_type == 'activity_funds':
            return "Activity Funds"
        else:
            return "Payment Receipt"

# Model for storing notification details
STUDENT_NOTIFICATION_TYPES = [
    ('arrival', 'Arrival'),
    ('departure', 'Departure'),
    ('fee_payment', 'Fee Payment'),
    ('activity', 'Activity'),
    ('activity_fee', 'Activity Fee'),
]

PARENT_NOTIFICATION_TYPES = [
    ('fee_payment', 'Fee Payment'),
    ('activity', 'Activity'),
    ('activity_fee', 'Activity Fee'),
    ('inventory_deficit', 'Inventory Deficit'),
    ('worker_leave', 'Worker Leave'),
    ('teacher_leave', 'Teacher Leave'),
]

class Notification(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=STUDENT_NOTIFICATION_TYPES)
    message = models.TextField()

    def __str__(self):
        return self.notification_type
    
class ParentNotification(models.Model):
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=PARENT_NOTIFICATION_TYPES)
    message = models.TextField()

    def __str__(self):
        return self.notification_type