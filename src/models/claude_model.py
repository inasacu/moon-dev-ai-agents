"""
🌙 Moon Dev's Claude Model Implementation
Built with love by Moon Dev 🚀
"""

from anthropic import Anthropic
from termcolor import cprint
from .base_model import BaseModel, ModelResponse
from .token_tracker import token_tracker

class ClaudeModel(BaseModel):
    """Implementation for Anthropic's Claude models"""
    
    AVAILABLE_MODELS = {
        # Claude 4 Series (New Generation) - 🌙 Moon Dev's Latest Models!
        "claude-opus-4-5-20251101": "Claude Opus 4.5 - Most powerful model with superior reasoning and creativity",
        "claude-opus-4-1": "Most powerful Claude 4 model with advanced reasoning",
        "claude-sonnet-4-5": "Balanced Claude 4.5 model with improved capabilities",
        "claude-haiku-4-5": "Fast, efficient Claude 4.5 model for rapid responses",

        # Claude 3 Series (Current Stable)
        "claude-3-5-sonnet-latest": "Latest Claude 3.5 Sonnet with enhanced performance",
        "claude-3-5-haiku-latest": "Latest Claude 3.5 Haiku - blazing fast",
        "claude-3-opus": "Most powerful Claude 3 model",
        "claude-3-sonnet": "Balanced Claude 3 model",
        "claude-3-haiku": "Fast, efficient Claude 3 model"
    }
    
    def __init__(self, api_key: str, model_name: str = "claude-3-haiku", **kwargs):
        self.model_name = model_name
        super().__init__(api_key, **kwargs)
    
    def initialize_client(self, **kwargs) -> None:
        """Initialize the Anthropic client"""
        try:
            self.client = Anthropic(api_key=self.api_key)
            cprint(f"✨ Initialized Claude model: {self.model_name}", "green")
        except Exception as e:
            cprint(f"❌ Failed to initialize Claude model: {str(e)}", "red")
            self.client = None
    
    def generate_response(self,
        system_prompt: str,
        user_content: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        agent_name: str = "unknown",
        **kwargs
    ) -> ModelResponse:
        """Generate a response using Claude"""
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_content}
                ]
            )

            # Log token usage for tracking
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            token_tracker.log_usage(
                model_name=self.model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                agent_name=agent_name
            )

            return ModelResponse(
                content=response.content[0].text.strip(),
                raw_response=response,
                model_name=self.model_name,
                usage={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                }
            )

        except Exception as e:
            cprint(f"❌ Claude generation error: {str(e)}", "red")
            raise
    
    def is_available(self) -> bool:
        """Check if Claude is available"""
        return self.client is not None
    
    @property
    def model_type(self) -> str:
        return "claude" 