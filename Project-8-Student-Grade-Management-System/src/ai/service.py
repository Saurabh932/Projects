from huggingface_hub import InferenceClient
from src.config.config import config
from fastapi.concurrency import run_in_threadpool
import logging
import re

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = InferenceClient(token=config.HF_TOKEN)
        # Zephyr is excellent at following strict formatting like bullet points
        self.model_id = "HuggingFaceH4/zephyr-7b-beta" 

    def _get_grade_info(self, grade: str) -> dict:
        """Returns grade header and its specific description point."""
        templates = {
            "A": {"header": "Grade A — Excellent Performance", "desc": "Displays exceptional mastery of the curriculum."},
            "B": {"header": "Grade B — Good Performance", "desc": "Displays good overall academic performance with balanced knowledge."},
            "C": {"header": "Grade C — Satisfactory Performance", "desc": "Meets basic academic expectations with average performance across subjects."},
            "F": {"header": "Grade F — Needs Improvement", "desc": "Academic performance is currently below expected standards."}
        }
        return templates.get(grade.upper(), {"header": f"Grade {grade}", "desc": "Performance review in progress."})

    def _get_local_analysis(self, subjects_text: str) -> list:
        """Fallback logic returning a list of bullet points."""
        scores = re.findall(r'([a-zA-Z\s]+):\s*(\d+)', subjects_text)
        if not scores:
            return ["• Strengths: General academic participation", "• Improvement: Focus on core fundamentals"]
        
        parsed = [(s[0].strip(), int(s[1])) for s in scores]
        strengths = [s[0] for s in parsed if s[1] >= 75]
        weakness = [s[0] for s in parsed if s[1] < 55]
        
        s_str = ", ".join(strengths) if strengths else "General consistency"
        w_str = ", ".join(weakness) if weakness else "Maintaining current standards"
        
        return [f"• Strengths: {s_str}", f"• Improvement: {w_str}"]

    async def generate_student_summary(self, data: dict) -> str:
        grade_info = self._get_grade_info(data['grade'])
        
        prompt = (
            f"<s>[INST] Analyze these grades: {data['subjects']}\n"
            f"Return exactly two lines starting with '•'.\n"
            f"• Strengths: [list subjects]\n"
            f"• Improvement: [list subjects] [/INST]"
        )

        try:
            response = await run_in_threadpool(
                self.client.text_generation,
                prompt,
                max_new_tokens=50,
                model=self.model_id,
                timeout=8,
                return_full_text=False
            )
            # Ensure AI output is split into clean lines
            ai_lines = [f"• {line.strip().lstrip('• ')}" for line in response.strip().split('\n') if line.strip()]
            if len(ai_lines) < 2:
                raise ValueError("Incomplete AI response")
        except Exception:
            ai_lines = self._get_local_analysis(data['subjects'])

        # BUILD THE FINAL LIST
        final_output = [
            grade_info['header'],
            f"• {grade_info['desc']}",  # Added bullet here
            ai_lines[0],               # Strengths bullet
            ai_lines[1],               # Improvement bullet
            "• Regular practice and structured study routines are recommended." # Added bullet here
        ]

        return "\n".join(final_output)

