from rest_framework import viewsets
from .serializers import FeedbackSerializer
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
from .models import Feedback

# views.py


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    
    def create(self, request, *args, **kwargs):
        task_id = self.request.data.get('task')
        existing_feedback = Feedback.objects.filter(task_id=task_id).first()

        if existing_feedback:
            serializer = self.get_serializer(existing_feedback)
            return JsonResponse(serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return JsonResponse(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Perform sentiment analysis and update worker's base_rating
        feedback_to_worker = serializer.validated_data.get('feedback_to_worker')
        feedback_to_client = serializer.validated_data.get('feedback_to_client')
        
        if feedback_to_worker is not None:
            return JsonResponse({"message": "You already Have given feedback to worker"})
        
        if feedback_to_client is not None:
            return JsonResponse({"message": "You already Have given feedback to client"})
            
        if feedback_to_worker:
            worker = instance.worker
            sentiment_score = analyze_sentiment(feedback_to_worker)
            
            # Update worker's base_rating
            update_worker_rating(worker, sentiment_score)

        self.perform_update(serializer)

        return JsonResponse(serializer.data)
    
    
def analyze_sentiment(text):
    # Implement your sentiment analysis logic here
    # You might want to use a pre-trained model or another approach
    
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)

    if scores['compound'] > 0.5:
        score = 50
    elif scores['compound'] > 0.1:
        score = 25
    elif scores['compound'] > -0.1:
        score = 0
    elif scores['compound'] > -0.5:
        score = -25
    else:
        score = -50
            
    return score

def update_worker_rating(worker, sentiment_score):
    # Update worker's base_rating based on sentiment_score
    # You might want to define a more sophisticated logic
    # For demonstration purposes, let's add the sentiment_score to the base_rating
    worker.base_rating += sentiment_score
    worker.save()