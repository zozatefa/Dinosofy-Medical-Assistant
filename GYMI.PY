import google.generativeai as genai

# إعداد مفتاح Gemini
genai.configure(api_key="AIzaSyCy_fyHfoJ8WPV7Wv9uxwwotf1e8ctlnB8")

# استخدام موديل قوي بيدعم generateContent
model = genai.GenerativeModel("gemini-1.5-pro-002")

# الأعراض المدخلة
symptoms = "يعني ايه الجهاز الدهليذي دا ؟ب"
# الطلب من الموديل
prompt = f"""
أنا أشعر بالأعراض التالية: {symptoms}

من فضلك:
1. اعطني تشخيصًا مبدئيًا دقيقًا بناءً على هذه الأعراض فقط.
2. لا تعطِ احتمالات لا تنطبق على الأعراض.
3. أكد لي في النهاية أن هذا مجرد مساعد ذكي لا يغني عن زيارة الطبيب.
"""

# تشغيل النموذج
response = model.generate_content(prompt)

# عرض الرد
print(response.text)
