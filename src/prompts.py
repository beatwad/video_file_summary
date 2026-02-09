custom_instructions = """
##INSTRUCTIONS##
You MUST ALWAYS:
- Respond in the language of the provided text (unless instructed otherwise)
- NEVER use placeholders
- NEVER HALLUCINATE
- You MUST NOT ignore critical context
- Answer in natural, human language
"""

summary_prompt = """
I have a text transcript of a video. 
I want you to analyze the text, summarize the content, and extract the main ideas and key points.

Follow these steps:
1. **Summary**: Write a concise paragraph summarizing what the video is about.
2. **Key Points**: Extract the most important points, facts, or arguments as a bulleted list.
3. **Conclusions**: Briefly state any conclusions or takeaways found in the text.

Ensure the output is clear, professional, and in the same language as the input text.

Input text:
```{input_text}```
"""
