
#prposition

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from django.http import HttpResponse
from django.shortcuts import render

# Initialisation du chatbot
bot = ChatBot('RestaurantBot', read_only=False,
              logic_adapters=[
                {
                    'import_path':'chatterbot.logic.BestMatch',
                    'default_response':'Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?',
                    'maximum_similarity_threshold': 0.85
                }
              ])

# Menu de notre restaurant
menu = [
    "Pizza Margherita: 10 TND",
    "Pizza Végétarienne: 12 TND",
    "Lasagne: 14 TND",
    "Tiramisu: 6 TND",
    "Burger: 8 TND",
    "Salade César: 9 TND",
    "Poulet rôti: 13 TND",
    "Frites: 4 TND",
    "Chapati : 3 TND"
]



# Entraînement du bot avec des données d'exemple
training_data = [
    "Bonjour",
    "Bonjour, comment puis-je vous aider ?",
    "Je voudrais réserver une table",
    "Pour combien de personnes ?",
    "Pour deux personnes",
    "À quelle heure voulez-vous réserver ?",
    "Pour 19h",
    "Très bien, c'est noté. Voulez-vous un coin tranquille ou plutôt animé ?",
    "Un coin tranquille ",
    "C'est noté, votre réservation est confirmée pour deux personnes à 19h dans un coin tranquille.",
    "Je voudrais commander pour livraison",
    "Bien sûr, nous proposons la livraison. Pouvez-vous nous donner votre adresse s'il vous plaît ?",
    "Je suis à l'adresse 123 rue du Bourguiba Monastir",
    "Merci, nous allons préparer votre commande et vous l'envoyer à l'adresse 123 rue du Bourguiba Monastir dans les plus brefs délais. Souhaitez-vous consulter notre menu en attendant ?",
    "Oui, je veux consulter le menu",
    "Voici notre menu : [`$menu`]",
    "Merci",
    "Très bien, n'hésitez pas à nous contacter si vous avez des questions ou des demandes spécifiques. Bonne journée !"
]

trainer = ListTrainer(bot)
trainer.train(training_data)

chatterbotcorpustrainer = ChatterBotCorpusTrainer(bot)
chatterbotcorpustrainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.french.greetings",
    "chatterbot.corpus.french.conversations",
    "chatterbot.corpus.french.trivia",
    "chatterbot.corpus.french.botprofile"
)
#chatterbotcorpustrainer.train('chatterbot.corpus.french')

# Fonction pour afficher le menu
def afficher_menu():
    # Concaténation des éléments de la liste menu
    menu_string = "\n".join(menu)
    # Formatage de la réponse
    response = "\nVoici notre menu :\n{}\n".format(menu_string)
    # Retourne la réponse formatée
    return response

# Fonction pour gérer les demandes de réservation de table



def reserver_table(nombre_personnes, heure, coin):
    
    nombre_max_places=50  # pour accéder à la variable globale dans la fonction
    
    # Vérification de la disponibilité de la table
    if coin == 'tranquille':
        # Simulation de la disponibilité de la table
        table_disponible = nombre_personnes <= nombre_max_places
        # Si la table est disponible, on confirme la réservation
        if table_disponible:
            nombre_max_places -= nombre_personnes
            confirmation = f"Nous avons bien reçu votre demande de réservation pour {nombre_personnes} personnes à {heure} dans le coin {coin}. Votre table est bien réservée."
        # Sinon, on informe le client que la table n'est pas disponible
        else:
            confirmation = f"Désolé, nous n'avons plus de tables disponibles pour {heure} dans le coin {coin}."
    # Si le coin choisi n'existe pas, on informe le client
    #else:
       # confirmation = f"Désolé, nous ne proposons pas de coin {coin} dans notre établissement."
    
    # Retour de la confirmation de réservation
    return confirmation



def getResponse(request):
    if request.method == 'GET':
        userMessage = request.GET.get('userMessage')
        if 'menu' in userMessage.lower():
            chatResponse = afficher_menu()
        #elif 'reservation' in userMessage.lower():
            # nombre_personnes = request.GET.get('nombre_personnes')
            # heure = request.GET.get('heure')
            # coin = request.GET.get('coin')
            # chatResponse = reserver_table(nombre_personnes, heure, coin)
        else:
            response = bot.get_response(userMessage)
            if response.confidence > 0.5:
                chatResponse = str(response)
            else:
                chatResponse = 'Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?'
        return HttpResponse(chatResponse)
    else:
         return HttpResponse('Invalid request method')


# 2 ém test je peux le supp
# import spacy
# from spacy.matcher import Matcher
# from spacy.tokens import Span
# from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
# from django.http import HttpResponse
# from django.shortcuts import render

# # Initialisation du chatbot
# bot = ChatBot('RestaurantBot', read_only=False,
#               logic_adapters=[
#                 {
#                     'import_path':'chatterbot.logic.BestMatch',
#                     'default_response':'Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?',
#                     'maximum_similarity_threshold': 0.85
#                 }
#               ])


# # Menu de notre restaurant
# menu = [
#     "Pizza Margherita: 10 TND",
#     "Pizza Végétarienne: 12 TND",
#     "Lasagne: 14 TND",
#     "Tiramisu: 6 TND",
#     "Burger: 8 TND",
#     "Salade César: 9 TND",
#     "Poulet rôti: 13 TND",
#     "Frites: 4 TND",
#     "Chapati : 3 TND"
# ]



# # Entraînement du bot avec des données d'exemple
# training_data = [
#     "Bonjour",
#     "Bonjour, comment puis-je vous aider ?",
#     "Je voudrais réserver une table",
#     "Pour combien de personnes ?",
#     "Pour deux personnes s'il vous plaît",
#     "À quelle heure voulez-vous réserver ?",
#     "Pour 19h",
#     "Très bien, c'est noté. Voulez-vous un coin tranquille ou plutôt animé ?",
#     "Un coin tranquille s'il vous plaît",
#     "C'est noté, votre réservation est confirmée pour deux personnes à 19h dans un coin tranquille.",
#     "Je voudrais commander pour livraison",
#     "Bien sûr, nous proposons la livraison. Pouvez-vous nous donner votre adresse s'il vous plaît ?",
#     "Je suis à l'adresse 123 rue du Paradis",
#     "Merci, nous allons préparer votre commande et vous l'envoyer à l'adresse 123 rue du Paradis dans les plus brefs délais. Souhaitez-vous consulter notre menu en attendant ?",
#     "Oui, je veux consulter le menu",
#     "Voici notre menu : [`$menu`]",
#     "Très bien, n'hésitez pas à nous contacter si vous avez des questions ou des demandes spécifiques. Bonne journée !",

#     ]

# trainer = ListTrainer(bot)
# trainer.train(training_data)

# chatterbotcorpustrainer = ChatterBotCorpusTrainer(bot)
# chatterbotcorpustrainer.train('chatterbot.corpus.french')


# # Fonction pour afficher le menu
# def afficher_menu():
#     # Concaténation des éléments de la liste menu
#     menu_string = "\n".join(menu)
#     # Formatage de la réponse
#     response = "\nVoici notre menu :\n{}\n".format(menu_string)
#     # Retourne la réponse formatée
#     return response

# # Fonction principale du chatbot
# def chatbot():
#     # Message d'accueil du chatbot
#     print("Bonjour ! Je suis un chatbot de restaurant. Comment puis-je vous aider ?")
#     # Boucle principale du chatbot
#     while True:
#         # Lecture de l'entrée de l'utilisateur
#         user_input = input("User: ")
#         # Vérification de l'entrée de l'utilisateur
#         if "menu" in user_input.lower():
#             # Appel de la fonction afficher_menu pour afficher le menu
#             print(afficher_menu())
#         elif "livraison" in user_input.lower():
#             print("Nous proposons la livraison en ligne via notre site web.")

#         elif "au revoir" in user_input.lower():
#             print("Au revoir !")
#             break
#         else:
#             #print("Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?")
#             trainer = ListTrainer(bot)
#             trainer.train(training_data)

#             chatterbotcorpustrainer = ChatterBotCorpusTrainer(bot)
#             chatterbotcorpustrainer.train('chatterbot.corpus.french')



# def getResponse(request):
#     if request.method == 'GET':
#         userMessage = request.GET.get('userMessage')
#         if 'menu' in userMessage.lower():
#             chatResponse = menu
#         else:
#             response = bot.get_response(userMessage)
#             if response.confidence > 0.5:
#                 chatResponse = str(response)
#             else:
#                 chatResponse = 'Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?'
#         return HttpResponse(chatResponse)
#     else:
         # return HttpResponse('Invalid request method')

 #1 er code juste



# """
# menu = [
#     "Pizza Margherita: 10 TND",
#     "Pizza Végétarienne: 12 TND ",
#     "Lasagne: 14 TND",
#     "Tiramisu: 6 TND",
#     "Burger: 8 TND",
#     "Salade César: 9 TND",
#     "Poulet rôti: 13 TND",
#     "Frites: 4 TND",
#     "chapati : 3 TND"
# ]

# response = "\nVoici notre menu :\n\n{}\n".format('\n'.join(menu))
# """




# # Entraînement du bot avec des données d'exemple
# training_data = [
#     "Bonjour",
#     "Bonjour, comment puis-je vous aider ?",
#     "Je voudrais réserver une table",
#     "Pour combien de personnes ?",
#     "Pour deux personnes s'il vous plaît",
#     "À quelle heure voulez-vous réserver ?",
#     "Pour 19h",
#     "Très bien, c'est noté. Voulez-vous un coin tranquille ou plutôt animé ?",
#     "Un coin tranquille s'il vous plaît",
#     "C'est noté, votre réservation est confirmée pour deux personnes à 19h dans un coin tranquille. Au revoir !",
#     "Je voudrais commander pour livraison",
#     "Bien sûr, nous proposons la livraison. Pouvez-vous nous donner votre adresse s'il vous plaît ?",
#     "Je suis à l'adresse 123 rue du Paradis",
#     "Merci, nous allons préparer votre commande et vous l'envoyer à l'adresse 123 rue du Paradis dans les plus brefs délais. Souhaitez-vous consulter notre menu en attendant ?",
#     "Oui, je veux consulter le menu",
#     "Voici notre menu : [`$menu`]",
#     "Très bien, n'hésitez pas à nous contacter si vous avez des questions ou des demandes spécifiques. Bonne journée !",

#     ]

# trainer = ListTrainer(bot)
# trainer.train(training_data)

# chatterbotcorpustrainer = ChatterBotCorpusTrainer(bot)
# chatterbotcorpustrainer.train('chatterbot.corpus.french')




# # Fonction pour répondre aux requêtes du client
# def getResponse(request):
#     if request.method == 'GET':
#         userMessage = request.GET.get('userMessage')
#         if 'menu' in userMessage.lower():
#             chatResponse = menu
#         else:
#             response = bot.get_response(userMessage)
#             if response.confidence > 0.5:
#                 chatResponse = str(response)
#             else:
#                 chatResponse = 'Désolé, je ne comprends pas. Pouvez-vous reformuler votre question ?'
#         return HttpResponse(chatResponse)
#     else:
#         return HttpResponse('Invalid request method')

def index(request):
    return render(request, 'blog/index.html')

def specific(request):
    list = [1,2,3]
    return HttpResponse(list)
