from mlx_lm import load, generate
from transformers import AutoTokenizer

class Translator:
    def __init__(self, model_path="google/translategemma-4b-it"):
        print(f"Loading TranslateGemma model: {model_path}...")
        # Load model with mlx-lm
        self.model, self.mlx_tokenizer = load(model_path)
        
        # Load full tokenizer from transformers for robust chat template handling
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("TranslateGemma model loaded.")

    def translate(self, text, source_lang, target_lang="en"):
        if not text or not text.strip():
            return ""

        # Map Whisper language codes to TranslateGemma codes if necessary.
        # Whisper returns 2-letter iso codes usually (e.g. 'zh', 'en').
        # TranslateGemma expects similar codes.
        
        # Handle Chinese specially if needed, but 'zh' is usually fine.
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "source_lang_code": source_lang,
                        "target_lang_code": target_lang,
                        "text": text,
                    }
                ],
            }
        ]
        
        try:
            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            
            # Generate translation
            response = generate(self.model, self.mlx_tokenizer, prompt=prompt, verbose=False, max_tokens=512)
            return response.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text # Fallback to original text
