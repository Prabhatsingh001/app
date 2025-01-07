from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CGPACalculatorSerializer
from rest_framework.exceptions import APIException

class CGPACalculatorView(APIView):
    def post(self, request):
        try:
            serializer = CGPACalculatorSerializer(data=request.data)
            if serializer.is_valid():
                semesters = serializer.validated_data['semesters']
                total_credits = 0
                weighted_sum = 0

                for semester in semesters:
                    sgpa = semester['sgpa']
                    credits = semester['credits']
                    weighted_sum += sgpa * credits
                    total_credits += credits

                if total_credits == 0:
                    return Response({'error': 'Total credits cannot be zero.'},status=status.HTTP_400_BAD_REQUEST)

                cgpa = weighted_sum / total_credits
                return Response({'cgpa': round(cgpa, 2)}, status=status.HTTP_200_OK)
        
            return Response({
                "error": {
                    "message": "Validation failed",
                    "details": serializer.errors,
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(f"An unexpected error occured : {str(e)}")
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequiredSGPASerializer

class RequiredSGPAView(APIView):
    def post(self, request):
        serializer = RequiredSGPASerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            completed_semesters = data['completed_semesters']
            total_program_credits = data['total_program_credits']
            future_semester_credits = data['future_semester_credits']
            expected_cgpa = data['expected_cgpa']

            # Calculate Required SGPA
            total_completed_credits = sum(sem['credits'] for sem in completed_semesters)
            total_weighted_sgpa = sum(sem['sgpa'] * sem['credits'] for sem in completed_semesters)

            required_cgpa_sum = expected_cgpa * total_program_credits
            required_weighted_sum = required_cgpa_sum - total_weighted_sgpa

            if future_semester_credits <= 0:
                return Response({'error': 'Future semester credits must be greater than zero.'},
                                status=status.HTTP_400_BAD_REQUEST)

            required_sgpa = required_weighted_sum / future_semester_credits
            return Response({'required_sgpa': round(required_sgpa, 2)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


