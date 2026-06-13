from django.core.management.base import BaseCommand
from apps.ai_engine.ml.train import train_models

class Command(BaseCommand):
    help = 'Train AI models using seed data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Training models...')
        train_models()
        self.stdout.write(self.style.SUCCESS('Models trained successfully.'))
