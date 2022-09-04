from huggingface_hub.inference_api import InferenceApi
import os
API_KEY = "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"
inference = InferenceApi(repo_id="arpanghoshal/EmoRoBERTa",
                         token=API_KEY)
inputText = "I wanna eat some chicken rice right about now"
result = inference(inputs=inputText)
result = result[0]
finalStr = f"Top 3 emotions for: '{inputText}' \n"
counter = 0
for d in result:
  finalStr += f"{d['label']}: {d['score']} \n"
  counter += 1
  if counter == 3:
    break
print(finalStr)
