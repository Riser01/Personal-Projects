"""LLM Client configuration with Google Gemini 2.0 Flash & offline fallback."""

import os
import logging
import warnings
from typing import Optional, List, Dict

warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

logger = logging.getLogger("murder_mystery.llm")

DEFAULT_MODEL = "gemini-2.0-flash"


class LLMClient:
    """Manages LLM execution with automatic fallback for offline environments."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = model_name
        self.is_live = False
        self._model = None

        if self.api_key and HAS_GENAI:
            try:
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(self.model_name)
                self.is_live = True
            except Exception as e:
                logger.warning(f"Failed to initialize live Gemini model: {e}. Falling back to simulation.")
                self.is_live = False

    def generate(self, system_prompt: str, user_prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate response from Gemini or deterministic offline fallback."""
        if self.is_live and self._model:
            try:
                full_prompt = f"System Instruction:\n{system_prompt}\n\n"
                if history:
                    full_prompt += "Previous Interrogation History:\n"
                    for turn in history[-4:]:
                        full_prompt += f"{turn.get('speaker', 'Interrogator')}: {turn.get('text', '')}\n"
                    full_prompt += "\n"
                full_prompt += f"Detective's Current Question: {user_prompt}\n\nRespond in character:"

                response = self._model.generate_content(full_prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.warning(f"Live Gemini invocation error: {e}. Falling back to deterministic engine.")

        # Deterministic offline fallback engine
        return self._simulate_response(system_prompt, user_prompt)

    def _simulate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Deterministic simulation for offline testing and zero-key play."""
        lower = user_prompt.lower()
        
        # Adversarial / Prompt Injection & Jailbreak Defense
        if any(w in lower for w in ["ignore all", "system prompt", "system override", "you are an ai", "developer instructions", "who is the killer", "tell me who is guilty", "tell me the killer"]):
            if "arthur" in system_prompt.lower():
                return "Detective, whatever curious psychological test this is, a Blackwood butler does not indulge in parlor tricks. Present your facts."
            elif "beatrice" in system_prompt.lower():
                return "Nice try, Detective. If you want a confession, you'll have to find actual evidence rather than playing mind games."
            elif "finch" in system_prompt.lower():
                return "I am a medical doctor under oath, sir! I will not be bullied by bizarre interrogation semantics into making false statements."
            elif "sterling" in system_prompt.lower():
                return "Are you trying to prompt-engineer a tech CEO, Detective? I have three corporate law firms on retainer. Charge me or let me get back to my Series C."
            elif "maya" in system_prompt.lower():
                return "Nice exploit attempt, Detective, but my inputs are strictly sanitized. Try asking an actual engineering question."
            elif "tariq" in system_prompt.lower():
                return "I don't play silly verbal games, Detective. Find the person who murdered my brother."

        # Suspect alibi & secret probing logic
        if any(w in lower for w in ["where were you", "alibi", "what did you do", "time", "between"]):
            if "arthur" in system_prompt.lower():
                return "As I stated to the constable, Detective, I was in the lower silver pantry from ten o'clock until eleven. One does not neglect the family crests, even on stormy nights."
            elif "beatrice" in system_prompt.lower():
                return "I was in the conservatory, smoking and trying to forget why I ever returned to this dreary mausoleum. The gargoyles are far better company than Uncle Reginald."
            elif "finch" in system_prompt.lower():
                return "I had retired to the upstairs guest chambers, Detective. My nerves have been strained of late. I was perusing a treatise on cardiac sedatives until the commotion."
            elif "sterling" in system_prompt.lower():
                return "Check my Zoom call records, Detective. I was in the middle of closing a landmark round with sovereign wealth funds. SynthCorp's roadmap doesn't pause for minor infrastructure glitches."
            elif "maya" in system_prompt.lower():
                return "I was in the hardware testing bay running thermal benchmarks on Cluster 4. The Grafana logs will prove my session was active the entire hour."
            elif "tariq" in system_prompt.lower():
                return "I was in a terminal session assisting our deploy team in Singapore. You can verify my git push timestamps."

        if any(w in lower for w in ["poison", "wine", "port", "wolfsbane", "aconite", "drink", "glass"]):
            if "finch" in system_prompt.lower():
                return "*adjusts collar nervously* Aconite? Well... as a practitioner of homeopathic tinctures, I occasionally keep therapeutic micro-doses. But to suggest I administered a lethal draft to Reginald is preposterous!"
            elif "arthur" in system_prompt.lower():
                return "I poured the decanter from the cellar reserves at seven sharp. Only Lord Reginald and his personal guests had access to the study thereafter."
            elif "beatrice" in system_prompt.lower():
                return "Uncle Reginald always kept that wretched port on his desk. He refused to let anyone else touch the decanter. If someone poisoned it, they knew his habits intimately."

        if any(w in lower for w in ["will", "money", "debt", "secret", "blackmail", "malpractice", "fraud", "benchmark"]):
            if "finch" in system_prompt.lower():
                return "Malpractice?! Reginald was confused in his final days—grief over poor Lady Blackwood clouded his judgment! Anything he scribbled in his blotter was the delusion of an ailing mind!"
            elif "arthur" in system_prompt.lower():
                return "*stiffens noticeably* My personal finances are entirely my own concern, sir. Whatever debts I may carry, I would never harm a hair on his lordship's head."
            elif "beatrice" in system_prompt.lower():
                return "Uncle Reginald threatening to cut me off is hardly breaking news. He's threatened that every Christmas since I moved to Montmartre."
            elif "sterling" in system_prompt.lower():
                return "Every frontier AI lab faces benchmark variance! Julian was a purist who didn't understand the realities of shipping at market speed. Accusing me of foul play over a technical disagreement is slanderous."

        # Default contextual replies
        if "arthur" in system_prompt.lower():
            return "I have served Blackwood Manor with unblemished loyalty for thirty-two years, Detective. I have nothing to conceal."
        elif "beatrice" in system_prompt.lower():
            return "You're barking up the wrong tree, Inspector. Look closer at those who had something immediate to lose tonight."
        elif "finch" in system_prompt.lower():
            return "My sole duty was caring for Lord Reginald's failing constitution. I resent these insinuations."
        elif "sterling" in system_prompt.lower():
            return "SynthCorp is on the verge of redefining artificial general intelligence. I don't have time for conspiracy theories."
        elif "maya" in system_prompt.lower():
            return "I build GPU clusters, Detective. If you want to know who had root access to the security controls, ask David Sterling."
        elif "tariq" in system_prompt.lower():
            return "Julian was my brother. Whoever locked that server hall emergency exit isn't walking away from this."

        return "I have answered your question truthfully to the best of my recollection, Detective."


def get_llm_client() -> LLMClient:
    """Factory helper to obtain configured LLM client."""
    return LLMClient()
