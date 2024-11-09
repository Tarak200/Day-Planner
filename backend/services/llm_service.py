import asyncio
import logging
from transformers import pipeline
from models.request_models import LLMRequest
from models.response_models import LLMResponse

# Configure logging to include debug level and output to console
logging.basicConfig(level=logging.DEBUG)

class LLMService:
    def __init__(self, model="gpt2", tokenizer="gpt2"):
        try:
            self.generator = pipeline(
                'text-generation',
                model=model,
                tokenizer=tokenizer,
                device=1  # Use CPU for compatibility
            )
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error("Error initializing generator:", exc_info=True)
            raise

    async def process_request(self, request: LLMRequest) -> LLMResponse:
        """Process the LLMRequest and return an LLMResponse."""
        try:
            # Construct the prompt based on the conversation history and query
            prompt = self.construct_prompt(request.conversation, request.query)
            logging.debug(f"Constructed prompt: {prompt}")
            
            # Generate the response asynchronously
            response_text = await asyncio.to_thread(self.generate_text, prompt)
            
            if response_text is None:
                raise Exception("Failed to generate text from LLM.")
            
            # Return the response wrapped in an LLMResponse object
            return LLMResponse(response=response_text)
        except Exception as e:
            logging.error("Error in process_request:", exc_info=True)
            raise

    def construct_prompt(self, conversation, query):
        """Construct the prompt from conversation history and current query."""
        try:
            prompt = ''
            for interaction in conversation:
                role = interaction['role']
                content = interaction['content']
                prompt += f"{role}: {content}\n"
            prompt += f"User: {query}\nSystem:"
            logging.debug(f"Constructed prompt: {prompt}")
            return prompt
        except Exception as e:
            logging.error("Error in construct_prompt:", exc_info=True)
            raise

    def generate_text(self, prompt, max_length=1024, num_return_sequences=1):
        """Generate text based on a provided prompt using an LLM."""
        try:
            # Generate text without specifying pad_token_id
            response = self.generator(
                prompt,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
            )
            # Return the first generated text sequence, removing the prompt
            generated_text = response[0]['generated_text']
            # Extract the new text generated after the prompt
            new_text = generated_text[len(prompt):].strip()
            print("#########################################")
            print(new_text)
            print("#########################################")
            return new_text
        except Exception as e:
            logging.error("Error generating text from LLM:", exc_info=True)
            return None
