"""API views for CGPA and required SGPA calculations."""

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CGPACalculatorSerializer, RequiredSGPASerializer


class CGPACalculatorView(APIView):
    """Calculate a CGPA from semester SGPA and credit values."""

    def post(self, request):
        """Return the weighted CGPA for the submitted semesters."""

        try:
            serializer = CGPACalculatorSerializer(data=request.data)
            if serializer.is_valid():
                semesters = serializer.validated_data["semesters"]  # type: ignore
                total_credits = 0
                weighted_sum = 0

                for semester in semesters:
                    sgpa = semester["sgpa"]
                    credits = semester["credits"]
                    weighted_sum += sgpa * credits
                    total_credits += credits

                if total_credits == 0:
                    return Response(
                        {"error": "Total credits cannot be zero."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cgpa = weighted_sum / total_credits
                return Response({"cgpa": round(cgpa, 2)}, status=status.HTTP_200_OK)

            return Response(
                {
                    "error": {
                        "message": "Validation failed",
                        "details": serializer.errors,
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            raise APIException(f"An unexpected error occured : {str(e)}")


class RequiredSGPAView(APIView):
    """Calculate the SGPA needed to reach a target CGPA."""

    def post(self, request):
        """Return the required SGPA for the submitted target."""

        serializer = RequiredSGPASerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            completed_semesters = data["completed_semesters"]  # type: ignore
            total_program_credits = data["total_program_credits"]  # type: ignore
            future_semester_credits = data["future_semester_credits"]  # type: ignore
            expected_cgpa = data["expected_cgpa"]  # type: ignore

            # Calculate Required SGPA
            total_completed_credits = sum(sem["credits"] for sem in completed_semesters)  # noqa: F841
            total_weighted_sgpa = sum(
                sem["sgpa"] * sem["credits"] for sem in completed_semesters
            )

            required_cgpa_sum = expected_cgpa * total_program_credits
            required_weighted_sum = required_cgpa_sum - total_weighted_sgpa

            if future_semester_credits <= 0:
                return Response(
                    {"error": "Future semester credits must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            required_sgpa = required_weighted_sum / future_semester_credits
            return Response(
                {"required_sgpa": round(required_sgpa, 2)}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
