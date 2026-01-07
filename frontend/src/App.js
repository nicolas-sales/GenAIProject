// On importe useState depuis React
// useState permet de stocker et mettre à jour l'état du composant
import { useState } from "react";

// Composant principal de l'application
function App() {

  // --------------------
  // ÉTATS DE L'APPLICATION
  // --------------------

  // Question écrite ou dictée par l'utilisateur
  const [question, setQuestion] = useState("");

  // Réponse générée par le backend RAG
  const [answer, setAnswer] = useState("");

  // Liste des sources utilisées pour générer la réponse
  const [sources, setSources] = useState([]);

  // Indique si le micro est en train d'écouter
  const [listening, setListening] = useState(false);

  // Indique si une requête est en cours vers le backend
  const [loading, setLoading] = useState(false);

  // Message d'erreur éventuel
  const [error, setError] = useState("");

  // --------------------
  // 🎙️ RECONNAISSANCE VOCALE (Speech-to-Text)
  // --------------------

  // Cette fonction démarre l'écoute du micro
  // et transforme la voix de l'utilisateur en texte
  const startListening = () => {

    // Récupération de l'API Web Speech selon le navigateur
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    // Si le navigateur ne supporte pas la reconnaissance vocale
    if (!SpeechRecognition) {
      alert("Speech-to-Text non supporté par ce navigateur");
      return;
    }

    // Création de l'objet de reconnaissance vocale
    const recognition = new SpeechRecognition();

    // Pas de langue imposée :
    // le navigateur détecte automatiquement la langue
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    // Quand l'écoute commence, on met listening à true
    recognition.onstart = () => setListening(true);

    // Quand l'écoute s'arrête, on met listening à false
    recognition.onend = () => setListening(false);

    // Quand un résultat vocal est détecté
    recognition.onresult = (event) => {

      // Récupération du texte reconnu
      const transcript = event.results[0][0].transcript;

      // On remplit automatiquement le champ question
      setQuestion(transcript);
    };

    // Lancement de l'écoute
    recognition.start();
  };

  // --------------------
  // 🔊 SYNTHÈSE VOCALE (Text-to-Speech)
  // --------------------

  // Cette fonction lit la réponse à voix haute
  const speak = (text) => {

    // Vérifie si le navigateur supporte la synthèse vocale
    if (!window.speechSynthesis) {
      alert("Text-to-Speech non supporté par ce navigateur");
      return;
    }

    // Création de l'objet de synthèse vocale à partir du texte
    const utterance = new SpeechSynthesisUtterance(text);

    // Pas de langue imposée :
    // le navigateur choisit automatiquement la meilleure voix
    utterance.rate = 1;
    utterance.pitch = 1;

    // Lecture du texte
    window.speechSynthesis.speak(utterance);
  };

  // --------------------
  // 📡 APPEL AU BACKEND RAG (FastAPI)
  // --------------------

  // Cette fonction envoie la question au backend
  // et récupère la réponse et les sources
  const sendQuestion = async () => {

    // Empêche l'envoi d'une question vide
    if (!question.trim()) return;

    // Réinitialisation des états avant l'appel API
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      // Appel HTTP POST vers l'endpoint /ask
      const response = await fetch("http://127.0.0.1:8000/ask",{
        method: "POST",
        headers: { "Content-Type": "application/json" },

        // Le backend attend un JSON avec la clé "question"
        body: JSON.stringify({
          question: question
        })
      });

      // Si la réponse HTTP n'est pas correcte
      if (!response.ok) {
        throw new Error("Erreur serveur");
      }

      // Conversion de la réponse JSON
      const data = await response.json();

      // Mise à jour de la réponse et des sources
      setAnswer(data.answer);
      setSources(data.sources || []);

    } catch (err) {

      // Gestion des erreurs réseau ou serveur
      setError("Impossible de contacter l'API RAG");

    } finally {

      // Fin du chargement
      setLoading(false);
    }
  };

  // --------------------
  // INTERFACE UTILISATEUR (JSX)
  // --------------------

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        {/* Titre de l'application */}
        <h2 style={styles.title}>GenAI RAG Assistant</h2>

        {/* Champ de saisie de la question */}
        <label style={styles.label}>Question (écrite ou dictée)</label>
        <textarea
          rows="4"
          style={styles.textarea}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Écris ou parle ta question..."
        />

        {/* Bouton pour activer la reconnaissance vocale */}
        <button
          style={{
            ...styles.button,
            backgroundColor: listening ? "#dc2626" : "#16a34a"
          }}
          onClick={startListening}
        >
          {listening ? "🎙️ Écoute en cours..." : "🎙️ Parler"}
        </button>

        {/* Bouton pour envoyer la question au backend */}
        <button
          style={styles.button}
          onClick={sendQuestion}
          disabled={loading}
        >
          {loading ? "Recherche en cours..." : "Poser la question"}
        </button>

        {/* Affichage des erreurs */}
        {error && (
          <div style={styles.errorBox}>
            {error}
          </div>
        )}

        {/* Affichage de la réponse */}
        {answer && (
          <div style={styles.answerBox}>
            <strong>Réponse</strong>
            <p>{answer}</p>

            {/* Bouton pour lire la réponse à voix haute */}
            <button
              style={styles.listenButton}
              onClick={() => speak(answer)}
            >
              🔊 Lire la réponse
            </button>
          </div>
        )}

        {/* Affichage des sources utilisées par le RAG */}
        {sources.length > 0 && (
          <div style={styles.sourcesBox}>
            <strong>Sources</strong>
            <ul>
              {sources.map((src, index) => (
                <li key={index}>
                  {src.source_type.toUpperCase()} — {src.source_name}
                </li>
              ))}
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}

// Export du composant principal
export default App;


// --------------------
// STYLES (CSS-in-JS)
// --------------------
const styles = {
  page: {
    minHeight: "100vh",
    backgroundColor: "#f4f6f8",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  card: {
    backgroundColor: "white",
    padding: "30px",
    borderRadius: "10px",
    width: "420px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
  },
  title: {
    textAlign: "center",
    marginBottom: "20px",
  },
  label: {
    fontWeight: "bold",
    marginTop: "15px",
    display: "block",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    marginTop: "5px",
    resize: "none",
  },
  button: {
    width: "100%",
    marginTop: "15px",
    padding: "12px",
    backgroundColor: "#4f46e5",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "16px",
  },
  answerBox: {
    marginTop: "20px",
    padding: "15px",
    backgroundColor: "#eef2ff",
    borderRadius: "6px",
  },
  sourcesBox: {
    marginTop: "15px",
    padding: "10px",
    backgroundColor: "#f1f5f9",
    borderRadius: "6px",
    fontSize: "14px",
  },
  listenButton: {
    marginTop: "10px",
    padding: "10px",
    width: "100%",
    backgroundColor: "#0ea5e9",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  errorBox: {
    marginTop: "15px",
    padding: "10px",
    backgroundColor: "#fee2e2",
    color: "#991b1b",
    borderRadius: "6px",
  }
};


