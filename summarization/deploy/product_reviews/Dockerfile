# Include Python
from python:3.9

# Define your working directory
WORKDIR /

# Install runpod
RUN pip install runpod
RUN pip install --default-timeout=900 torch --index-url https://download.pytorch.org/whl/cu118
RUN pip install transformers

# Add your file
ADD predict.py .
ADD test_input.json .

# Call your file when your container starts
CMD [ "python", "-u", "/predict.py" ]