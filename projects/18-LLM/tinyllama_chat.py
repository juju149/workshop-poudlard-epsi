import ollama

def chat():
    print("="*60)
    print("Bienvenue dans le chat TinyLlama !")
    print("Le plus petit modèle performant en local (1.1B paramètres)")
    print("="*60)
    print("\nTapez 'quit' ou 'exit' pour quitter\n")
    
    conversation_history = []
    
    while True:
        try:
            user_input = input("Vous: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Au revoir !")
                break
            
            if not user_input.strip():
                continue
            
            # Ajouter le message de l'utilisateur à l'historique
            conversation_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Générer la réponse avec TinyLlama
            print("TinyLlama: ", end="", flush=True)
            
            full_response = ""
            response = ollama.chat(
                model='tinyllama',
                messages=conversation_history,
                stream=True
            )
            
            for chunk in response:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content
            
            print("\n")
            
            # Ajouter la réponse à l'historique
            conversation_history.append({
                'role': 'assistant',
                'content': full_response
            })
            
        except KeyboardInterrupt:
            print("\n\nAu revoir !")
            break
        except Exception as e:
            print(f"\nErreur : {e}")
            print("Assurez-vous que le serveur Ollama est lancé avec: ollama serve\n")

if __name__ == "__main__":
    chat()
