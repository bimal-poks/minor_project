from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Student, Session, AttendanceRecord
from .serializers import StudentSerializer, SessionSerializer, AttendanceRecordSerializer


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class SessionListCreateView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


@api_view(['POST'])
def mark_attendance(request):
    roll_number = request.data.get('roll_number')
    session_id = request.data.get('session_id')

    if not roll_number or not session_id:
        return Response(
            {"error": "roll_number and session_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        student = Student.objects.get(roll_number=roll_number)
        session = Session.objects.get(id=session_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
    except Session.DoesNotExist:
        return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    record, created = AttendanceRecord.objects.get_or_create(
        student=student,
        session=session,
        defaults={"status": "present"}
    )

    if not created:
        return Response(
            {"message": f"{student.name} already marked present for this session",
             "duplicate": True},
            status=status.HTTP_200_OK
        )

    serializer = AttendanceRecordSerializer(record)
    return Response(
        {"message": f"{student.name} marked present", "record": serializer.data},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def attendance_report(request):
    records = AttendanceRecord.objects.all()

    date = request.query_params.get('date')
    session_id = request.query_params.get('session_id')
    student_id = request.query_params.get('student_id')

    if date:
        records = records.filter(session__date=date)
    if session_id:
        records = records.filter(session_id=session_id)
    if student_id:
        records = records.filter(student_id=student_id)

    serializer = AttendanceRecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def today_summary(request):
    today = timezone.localdate()
    records = AttendanceRecord.objects.filter(session__date=today)
    serializer = AttendanceRecordSerializer(records, many=True)
    return Response({
        "date": str(today),
        "count": records.count(),
        "records": serializer.data
    })
