from googletrans import Translator

def translate_text(text, target_lang):
    translator = Translator()
    # print("Translating")
    translated_text = translator.translate(text, dest=target_lang)
    # print(translated_text.text)
    return translated_text.text

# print(translate_text("मेरा नाम पीयूष है.और मैं आपको एक lottery का number भेज रहा हूं.आपके account मेंपचास हज़ार रुपए आ सकते हैंबस आप मुझेआपके number पर जो OTP आया हैवह कृपया send कर दीजिए.देखनहीं हो रहारुक रुक अगर तेरे को बोलने के दो second रुको.बोल सकता हैमेरा मेरा mic monitorपर वह नहीं हो रहा नहीं हो रहा नहीं हो रहानहीं करता रहे वह मैंने देखा है.देख एक बार बोल.नहीं नहीं रुक रुक रुक दो second रुक.Mic मेरा मेरा रहने था मेरा जो speaker है ना वह BenQबोला अभी.बहुत बार ही हो गए. अभी वह same font कर दिया ना जो तुझे चाहिएथा और वहहां कर सकता है कर सकता है.हां, उसकेबातकितनाकितना भी कितना भी कितनावह वह मैंने flex कियाकि वह तो नीचे होते जा रहे हैंवह, तो जितना भी बोलेवह जो भी और नीचे आएगा.मैं मैं अभी क्या कर रहा हूं क्या बैठ के?मैं अभी top 10 scam calls के यह data निकल रहाऔर हम कल उनको बोलेंगे कि यह top 10 है worldwide.तो और वही हमबोलेंगे prompt को.वह अभीचल रहा है बैठ के अभी.ठीक हैतो अच्छा हो रहा है.", "en"))
# print(translate_text("आपका बैंक खाता बंद होने वाला है।", "en"))

