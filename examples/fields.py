from django.db.models.fields.files import ImageField
from django.core.files import File
from PIL import Image
import io

class CompressedImageField(ImageField):
    def __init__(self, *args, **kwargs):
        self.quality = kwargs.pop('quality', 60)  # Default quality is 60%
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        
        if file and hasattr(file, 'content_type') and file.content_type.startswith('image'):
            # Open the image using PIL
            img = Image.open(file)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a BytesIO object to store the compressed image
            output = io.BytesIO()
            
            # Save the image with compression
            img.save(output, format='JPEG', quality=self.quality, optimize=True)
            output.seek(0)
            
            # Create a new Django File object
            compressed_file = File(output, name=file.name)
            
            # Set the file field to the compressed file
            setattr(model_instance, self.attname, compressed_file)
            
            return compressed_file
        return file 