import os
import sys
import re
import signal
import threading
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv  

# Créer une console Rich pour l'affichage formaté
console = Console()

# Variable globale pour suivre si une génération est en cours
generation_en_cours = False
stop_generation = False

def signal_handler(sig, frame):
    """Gestionnaire de signal pour CTRL+C pendant la génération"""
    global stop_generation
    if generation_en_cours:
        stop_generation = True
        print("\n\n[Interruption de la génération...]")
        return
    else:
        # Comportement par défaut (quitter le programme)
        sys.exit(0)

def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def render_markdown(text):
    """Affiche du texte formaté en Markdown"""
    console.print(Markdown(text))

def main():
    # Configuration du gestionnaire de signal pour CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        import rich
    except ImportError:
        print("Installation de la bibliothèque 'rich'...")
        os.system('pip install rich')
    
    try:
        import dotenv
    except ImportError:
        print("Installation de la bibliothèque 'python-dotenv'...")
        os.system('pip install python-dotenv')
    
    # Charger les variables d'environnement
    load_dotenv()
    
    endpoint = os.getenv('AZURE_ENDPOINT')
    model_name = os.getenv('AZURE_MODEL')
    api_key = os.getenv('AZURE_API_KEY')
    
    if not endpoint or not model_name or not api_key:
        console.print("❌ Erreur: Variables d'environnement manquantes dans le fichier .env", style="bold red")
        console.print("Assurez-vous que les variables AZURE_ENDPOINT, AZURE_MODEL et AZURE_API_KEY sont définies.", style="yellow")
        return
    
    client = None  
    
    try:
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key),
        )
        
        conversation = [
            SystemMessage(content="You are a helpful assistant that responds concisely and accurately.")
        ]
        
        clear_screen()
        console.print("="*50, style="bold cyan")
        console.print(f"💬 DeepSeek Terminal Chat ({model_name} via Azure)", style="bold green")
        console.print("="*50, style="bold cyan")
        console.print("• Tapez votre message et appuyez sur Entrée pour discuter", style="yellow")
        console.print("• Tapez 'exit', 'quit' ou 'q' pour quitter", style="yellow")
        console.print("• Tapez 'clear' pour effacer la conversation", style="yellow")
        console.print("• Tapez 'save' pour sauvegarder la conversation", style="yellow")
        console.print("• Appuyez sur CTRL+C pendant la génération pour l'interrompre", style="yellow")
        console.print("="*50, style="bold cyan")
        
        while True:
            user_input = input("\n\033[1;36mVous:\033[0m ")
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                console.print("\nFin de la conversation. Au revoir! 👋", style="bold green")
                break
            elif user_input.lower() == 'clear':
                conversation = [SystemMessage(content="You are a helpful assistant that responds concisely and accurately.")]
                clear_screen()
                console.print("🧹 Conversation effacée.", style="bold green")
                continue
            elif user_input.lower() == 'save':
                with open(f"deepseek_conversation_{os.getpid()}.txt", "w", encoding="utf-8") as f:
                    for msg in conversation:
                        if hasattr(msg, 'role'):
                            f.write(f"{msg.role}: {msg.content}\n\n")
                        else:
                            f.write(f"{type(msg).__name__}: {msg.content}\n\n")
                console.print("💾 Conversation sauvegardée!", style="bold green")
                continue
            elif not user_input.strip():
                continue
                
            conversation.append(UserMessage(content=user_input))
            console.print("\n[bold green]DeepSeek:[/bold green] ", end="")
            
            try:
                global generation_en_cours, stop_generation
                generation_en_cours = True
                stop_generation = False
                
                response = client.complete(
                    stream=True,
                    messages=conversation,
                    max_tokens=2048,
                    temperature=0.7,
                    top_p=0.95,
                    model=model_name
                )
                
                full_response = ""
                
                for update in response:
                    if stop_generation:
                        console.print("\n[Génération interrompue par l'utilisateur]", style="bold red")
                        break
                        
                    if update.choices:
                        chunk = update.choices[0].delta.content or ""
                        full_response += chunk
                        print(chunk, end="")
                        sys.stdout.flush()
                
                # Ajouter la réponse à la conversation uniquement si elle n'est pas vide
                if full_response.strip():
                    conversation.append(AssistantMessage(content=full_response))
                    
                    print("\n")
                    console.print("--- Version formatée ---", style="dim cyan")
                    render_markdown(full_response)
                    console.print("---", style="dim")
                else:
                    console.print("\nLa génération n'a pas produit de réponse.", style="yellow")
                
            except Exception as e:
                console.print(f"\n❌ Erreur: {str(e)}", style="bold red")
            finally:
                generation_en_cours = False
    
    except Exception as e:
        console.print(f"Erreur d'initialisation: {str(e)}", style="bold red")
    
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\nInterruption utilisateur. Au revoir! 👋", style="bold yellow")
    except Exception as e:
        console.print(f"Erreur inattendue: {str(e)}", style="bold red")