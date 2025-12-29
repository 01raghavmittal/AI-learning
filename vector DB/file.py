
import os, sys
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.exceptions import ClientAuthenticationError

from dotenv import load_dotenv
load_dotenv()


ENDPOINT = os.getenv("VISION_ENDPOINT", "").rstrip("/")
KEY = os.getenv("VISION_KEY", "")

if not ENDPOINT or "cognitiveservices.azure.com" not in ENDPOINT:
    print("[ERROR] VISION_ENDPOINT must be your Computer Vision endpoint, e.g. https://<name>.cognitiveservices.azure.com", file=sys.stderr); sys.exit(1)
if not KEY or len(KEY.strip()) < 20:
    print("[ERROR] VISION_KEY is missing or looks wrong. Use Key1/Key2 from the same resource.", file=sys.stderr); sys.exit(1)

client = ImageAnalysisClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

with open("presentation.png", "rb") as f:
    image_bytes = f.read()

try:
    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.READ],
        language="en",
    )
    if result.read and result.read.blocks:
        print("Detected text:")
        for b in result.read.blocks:
            for line in b.lines:
                print(line.text)
    else:
        print("No text detected.")
except ClientAuthenticationError as e:
    print("[401 AUTH ERROR] Check that your key and endpoint belong to the SAME Computer Vision resource and region.", file=sys.stderr)
    print(e, file=sys.stderr)
