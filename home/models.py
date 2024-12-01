from django.db import models

class EmailBatch(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sender_email = models.EmailField(help_text="Email address of the sender", null=True, blank= True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email Batch - {self.subject}"


class SMSBatch(models.Model):
    message = models.TextField()
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SMS Batch - {self.message[:30]}"


# from django.db import models

# class EmailBatch(models.Model):
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Email Batch - {self.subject}"
