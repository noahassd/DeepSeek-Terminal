
# 💬 DeepSeek Terminal Chat (Azure)

Un assistant conversationnel en ligne de commande basé sur le modèle **DeepSeek-V3** via Azure AI Inference.  
Cette interface permet de discuter avec un LLM et de sauvegarder ou effacer la conversation.

---

## 🚀 Fonctionnalités

- Connexion à l’API Azure AI avec `azure.ai.inference`
- Streaming des réponses token par token
- Affichage enrichi avec `rich` (et support du Markdown)
- Commandes intégrées :
  - `clear` : réinitialiser la conversation
  - `save` : sauvegarder la conversation dans un fichier `.txt`
  - `exit` / `quit` / `q` : quitter l’interface

---

## 🛠️ Prérequis

- Python 3.8+
- Un endpoint Azure AI Inference avec une clé API valide
- Clé et URL définies dans un fichier `.env`

---

## 📦 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/noahassd/DeepSeek-Terminal
cd DeepSeek-Terminal
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Créer un fichier `.env` à partir de l’exemple fourni :
```bash
cp .env.example .env
```

4. Modifier `.env` avec vos valeurs Azure :
```env
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=https://your-endpoint-url/models
AZURE_MODEL=DeepSeek-V3
```

---

## ▶️ Lancer l’application

```bash
python DeepSeek.py
```

---

## ✨ Aperçu Terminal

```bash
==================================================
💬 DeepSeek Terminal Chat (DeepSeek-V3 via Azure)
==================================================
• Tapez votre message et appuyez sur Entrée pour discuter
• Tapez 'exit', 'quit' ou 'q' pour quitter
• Tapez 'clear' pour effacer la conversation
• Tapez 'save' pour sauvegarder la conversation
• Appuyez sur CTRL+C pendant la génération pour l'interrompre
==================================================
```

---

## 🔐 Sécurité

> Ne stockez jamais votre clé API directement dans le script.  
Utilisez le fichier `.env` pour une gestion sécurisée.

---

## 📄 Licence

Distribué sous licence MIT.
