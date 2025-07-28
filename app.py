from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import wikipedia

app = Flask(__name__)
wikipedia.set_lang("tr")

@app.route("/", methods=["POST"])
def wikiBot():
    mesaj = request.form.get("Body")
    yanit = MessagingResponse()

    try:

        ozet = wikipedia.summary(mesaj, sentences=5)
        yanit.message(ozet)
    except wikipedia.exceptions.DisambiguationError as e:
        yanit.message("Daha spesifik bir şey söyler misin? Örneğin, Python: programlaam dili mi, piton mu?:"  + ", ".join(e.options[:3]))
    except wikipedia.exceptions.PageError:
        yanit.message("Başlığı bulamadık.")
    except Exception as e:
        yanit.message("Bir hata oluştu: " + str(e))
    return str(yanit)


if __name__ == "__main__":
    app.run(debug=True)