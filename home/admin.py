import phonenumbers
from django.contrib import admin
from .models import EmailBatch, SMSBatch
import pandas as pd
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

sender = settings.EMAIL_HOST_USER  # Replace with your actual sender email if different


@admin.register(EmailBatch)
class EmailBatchAdmin(admin.ModelAdmin):
    list_display = ('subject', 'uploaded_at')
    actions = ['send_bulk_emails', 'send_single_email']

    def send_bulk_emails(self, request, queryset):
        """
        Admin action to send emails to recipients in uploaded files for selected EmailBatch instances.
        """
        for batch in queryset:
            try:
                file = batch.file
                file_extension = file.name.split('.')[-1].lower()

                # Load file into a DataFrame
                if file_extension == 'csv':
                    df = pd.read_csv(file)
                elif file_extension in ['xls', 'xlsx']:
                    df = pd.read_excel(file)
                else:
                    self.message_user(
                        request, f"Unsupported file type in batch '{batch.subject}'.", level='error'
                    )
                    continue

                if 'email' not in df.columns:
                    self.message_user(
                        request, f"Missing 'email' column in batch '{batch.subject}'.", level='error'
                    )
                    continue

                # Send emails to valid addresses
                success_count = 0
                invalid_emails = []
                for email in df['email']:
                    if pd.isna(email) or '@' not in str(email):
                        invalid_emails.append(email)
                        continue

                    try:
                        send_mail(
                            subject=batch.subject,
                            message=batch.message,
                            from_email=batch.sender_email or sender,
                            recipient_list=[email.strip()],
                            fail_silently=False,
                        )
                        success_count += 1
                    except Exception as e:
                        self.message_user(
                            request, f"Error sending email to {email}: {e}", level='error'
                        )

                # Feedback to admin
                if invalid_emails:
                    self.message_user(
                        request,
                        f"Skipped {len(invalid_emails)} invalid emails in batch '{batch.subject}'.",
                        level='warning',
                    )
                self.message_user(
                    request,
                    f"Successfully sent {success_count} emails for batch '{batch.subject}'.",
                    level='success',
                )

            except Exception as e:
                self.message_user(
                    request, f"Error processing batch '{batch.subject}': {e}", level='error'
                )

    send_bulk_emails.short_description = "Send Bulk Emails for Selected Batches"
