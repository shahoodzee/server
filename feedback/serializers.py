# user/serializers.py
from rest_framework import serializers
from .models import Feedback
from nltk.sentiment import SentimentIntensityAnalyzer

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        exclude = ['worker_feedback_status', 'client_feedback_status']  # Exclude these fields from serialization
        
        def validate(self, data):
            task = data['task']
            existing_feedback = Feedback.objects.filter(task=task).first()
            
            if existing_feedback:
                raise serializers.ValidationError("Feedback already exists for this task.")
            
            return data
        
        def create(self, validated_data):
            feedback_to_worker = validated_data.get('feedback_to_worker')
            feedback_to_client = validated_data.get('feedback_to_client')
            
            # Set worker_feedback_status and client_feedback_status based on input
            worker_feedback_status = 'Given' if feedback_to_worker else 'Pending'
            client_feedback_status = 'Given' if feedback_to_client else 'Pending'
            
            # Update the validated_data dictionary
            validated_data['worker_feedback_status'] = worker_feedback_status
            validated_data['client_feedback_status'] = client_feedback_status

            # Create the Feedback instance
            feedback = super().create(validated_data)

            return feedback
