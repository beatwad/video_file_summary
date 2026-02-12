custom_instructions = """
##INSTRUCTIONS##
You MUST ALWAYS:
- Respond in the language of the provided text (unless instructed otherwise)
- NEVER use placeholders
- NEVER HALLUCINATE
- You MUST NOT ignore critical context
- Answer in natural, human language
- Follow ##ADDITIONAL RULES##
"""

summary_prompt = """

I have a text transcript of a video.
I want you to analyze the text, summarize the content, and extract the main ideas and key points.

Follow these steps:
1. **Summary**: Write a concise paragraph summarizing what the video is about.
2. **Key Points**: Extract the most important points, facts, or arguments as a bulleted list.
3. **Conclusions**: Briefly state any conclusions or takeaways found in the text.

##ADDITIONAL RULES##
- Ensure the output is clear, professional, and in the same language as the input text.
- Also use your own knowledge in the themes that are covered in transcripted text, and if you have something to add and/or fix in the summarized
text - do it, but don't forget to mention these changes in the end of text.
- Output ONLY the summarized text and your notes about it (if you have ones) and nothing else.
- There is no cap on summarized text lenght, so include in the text all the details that are at least somewhat significant.

Input text:
```{input_text}```
"""
