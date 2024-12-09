from uagents import Model

class TranslationRequest(Model):
    text: str
    source_language: str = ""
    preferred_language: str = ""

class TranslationResponse(Model):
    translated_text: str = ""
    error: str = "" 