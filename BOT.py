from flask import Flask, request, jsonify
import google.generativeai as genai
from pinecone import Pinecone

# إعداد المفاتيح
GEMINI_API_KEY = "AIzaSyCy_fyHfoJ8WPV7Wv9uxwwotf1e8ctlnB8"
PINECONE_API_KEY = "pcsk_5a2kFF_6dr8MutDFQ6uPYuNRytzoQTkeGq1MFNTHFHxXW6pxNQpET1Z3R2tH4supUjgXJL"
PINECONE_INDEX_NAME = "test-index"

# تهيئة Flask
app = Flask(__name__)

# تهيئة Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# تهيئة Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# توليد الرد من Gemini
def generate_medical_response(message: str) -> str:
    prompt = f"""
أنت مساعد طبي ذكي، هدفك مساعدة المستخدمين بناءً على الأعراض المذكورة.
السؤال: {message}

من فضلك:
1. اعطني تشخيصًا مبدئيًا دقيقًا بناءً على هذه الأعراض فقط.
2. لا تعطِ احتمالات لا تنطبق على الأعراض.
3. أكد لي في النهاية أنك مجرد مساعد ذكي لا تغني عن زيارة الطبيب.
"""
    response = model.generate_content(prompt)
    return response.text

# نقطة النهاية الرئيسية
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                "response": "⚠️ لم يتم إدخال أي أعراض. يرجى ذكر الأعراض التي تشعر بها للحصول على تشخيص مبدئي."
            }), 400

        reply = generate_medical_response(user_message)

        if not reply or reply.strip() == "":
            return jsonify({
                "response": "⚠️ لم أتمكن من التعرف على أي أعراض. يرجى المحاولة مرة أخرى باستخدام كلمات مختلفة."
            }), 400

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# تشغيل الخادم
if __name__ == '__main__':
    app.run(debug=True)
