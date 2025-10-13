import '../models/question.dart';

class QuizData {
  static List<Question> getQuestions() {
    return [
      // Question 1
      Question(
        text: "Quelle est votre qualité principale ?",
        answers: [
          Answer(text: "Courage", scores: {'gryffindor': 3, 'auror': 2}),
          Answer(text: "Ambition", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "Intelligence", scores: {'ravenclaw': 3}),
          Answer(text: "Loyauté", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 2
      Question(
        text: "Comment réagissez-vous face au danger ?",
        answers: [
          Answer(text: "Je fonce tête baissée", scores: {'gryffindor': 3, 'auror': 2}),
          Answer(text: "J'élabore un plan stratégique", scores: {'slytherin': 2, 'ravenclaw': 2}),
          Answer(text: "J'analyse la situation calmement", scores: {'ravenclaw': 3}),
          Answer(text: "Je protège mes amis d'abord", scores: {'hufflepuff': 3, 'gryffindor': 1}),
        ],
      ),
      // Question 3
      Question(
        text: "Quel sort aimeriez-vous maîtriser ?",
        answers: [
          Answer(text: "Expecto Patronum", scores: {'gryffindor': 2, 'auror': 3}),
          Answer(text: "Avada Kedavra", scores: {'dark_wizard': 4, 'slytherin': 1}),
          Answer(text: "Accio (sort d'Attraction)", scores: {'ravenclaw': 2, 'hufflepuff': 1}),
          Answer(text: "Protego (bouclier)", scores: {'hufflepuff': 2, 'auror': 2}),
        ],
      ),
      // Question 4
      Question(
        text: "Où préférez-vous passer votre temps libre ?",
        answers: [
          Answer(text: "Sur le terrain de Quidditch", scores: {'gryffindor': 3}),
          Answer(text: "Dans la Chambre des Secrets", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "À la bibliothèque", scores: {'ravenclaw': 3}),
          Answer(text: "Aux cuisines avec les elfes", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 5
      Question(
        text: "Quelle est votre matière préférée ?",
        answers: [
          Answer(text: "Défense contre les Forces du Mal", scores: {'gryffindor': 2, 'auror': 3}),
          Answer(text: "Potions", scores: {'slytherin': 3, 'ravenclaw': 1}),
          Answer(text: "Métamorphose", scores: {'ravenclaw': 3}),
          Answer(text: "Botanique", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 6
      Question(
        text: "Comment décririez-vous votre ambition ?",
        answers: [
          Answer(text: "Je veux devenir un héros", scores: {'gryffindor': 3, 'auror': 2}),
          Answer(text: "Je veux le pouvoir absolu", scores: {'slytherin': 3, 'dark_wizard': 3}),
          Answer(text: "Je veux tout savoir", scores: {'ravenclaw': 3}),
          Answer(text: "Je veux aider les autres", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 7
      Question(
        text: "Quel animal serait votre Patronus ?",
        answers: [
          Answer(text: "Un lion", scores: {'gryffindor': 3}),
          Answer(text: "Un serpent", scores: {'slytherin': 3, 'dark_wizard': 1}),
          Answer(text: "Un aigle", scores: {'ravenclaw': 3}),
          Answer(text: "Un blaireau", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 8
      Question(
        text: "Face à un choix difficile, vous...",
        answers: [
          Answer(text: "Suivez votre instinct", scores: {'gryffindor': 3}),
          Answer(text: "Choisissez ce qui vous avantage", scores: {'slytherin': 3}),
          Answer(text: "Pesez le pour et le contre", scores: {'ravenclaw': 3}),
          Answer(text: "Demandez conseil à vos amis", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 9
      Question(
        text: "Quelle est votre peur la plus profonde ?",
        answers: [
          Answer(text: "Échouer mes proches", scores: {'gryffindor': 2, 'hufflepuff': 2}),
          Answer(text: "Perdre le contrôle", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "L'ignorance", scores: {'ravenclaw': 3}),
          Answer(text: "La solitude", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 10
      Question(
        text: "Vous découvrez un secret dangereux. Que faites-vous ?",
        answers: [
          Answer(text: "Je le révèle pour protéger tout le monde", scores: {'gryffindor': 3, 'auror': 2}),
          Answer(text: "Je l'utilise à mon avantage", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "Je l'étudie avant de décider", scores: {'ravenclaw': 3}),
          Answer(text: "Je le partage avec mes amis de confiance", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 11
      Question(
        text: "Quel est votre style de duel magique ?",
        answers: [
          Answer(text: "Attaque directe et puissante", scores: {'gryffindor': 3, 'auror': 1}),
          Answer(text: "Sorts sombres et intimidants", scores: {'dark_wizard': 4, 'slytherin': 1}),
          Answer(text: "Tactique et précision", scores: {'ravenclaw': 3, 'slytherin': 1}),
          Answer(text: "Défense et protection", scores: {'hufflepuff': 2, 'auror': 2}),
        ],
      ),
      // Question 12
      Question(
        text: "Quelle baguette vous attirerait le plus ?",
        answers: [
          Answer(text: "Bois de houx et plume de phénix", scores: {'gryffindor': 3}),
          Answer(text: "Bois d'if et ventricule de dragon", scores: {'dark_wizard': 3, 'slytherin': 1}),
          Answer(text: "Bois de cerisier et crin de licorne", scores: {'ravenclaw': 3}),
          Answer(text: "Bois de chêne et poil de Kappa", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 13
      Question(
        text: "Votre approche du travail d'équipe ?",
        answers: [
          Answer(text: "Je prends naturellement le lead", scores: {'gryffindor': 2, 'slytherin': 2}),
          Answer(text: "Je préfère travailler seul", scores: {'dark_wizard': 3, 'ravenclaw': 1}),
          Answer(text: "J'apporte mes connaissances", scores: {'ravenclaw': 3}),
          Answer(text: "Je m'assure que chacun contribue", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 14
      Question(
        text: "Quelle relique de la mort choisiriez-vous ?",
        answers: [
          Answer(text: "La Baguette de Sureau (pouvoir)", scores: {'dark_wizard': 3, 'slytherin': 2}),
          Answer(text: "La Pierre de Résurrection (amour)", scores: {'hufflepuff': 3, 'gryffindor': 1}),
          Answer(text: "La Cape d'Invisibilité (sagesse)", scores: {'ravenclaw': 3, 'auror': 2}),
          Answer(text: "Aucune, c'est trop dangereux", scores: {'hufflepuff': 2, 'ravenclaw': 1}),
        ],
      ),
      // Question 15
      Question(
        text: "Votre créature magique préférée ?",
        answers: [
          Answer(text: "Dragon", scores: {'gryffindor': 2, 'dark_wizard': 2}),
          Answer(text: "Basilic", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "Phénix", scores: {'ravenclaw': 2, 'gryffindor': 2}),
          Answer(text: "Niffleur", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 16
      Question(
        text: "Comment gérez-vous les échecs ?",
        answers: [
          Answer(text: "Je recommence avec plus de détermination", scores: {'gryffindor': 3}),
          Answer(text: "Je cherche qui est responsable", scores: {'slytherin': 2, 'dark_wizard': 2}),
          Answer(text: "J'analyse ce qui n'a pas fonctionné", scores: {'ravenclaw': 3}),
          Answer(text: "Je demande de l'aide", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 17
      Question(
        text: "Quelle serait votre carrière idéale dans le monde magique ?",
        answers: [
          Answer(text: "Auror", scores: {'gryffindor': 2, 'auror': 4}),
          Answer(text: "Ministre de la Magie", scores: {'slytherin': 3}),
          Answer(text: "Professeur à Poudlard", scores: {'ravenclaw': 3, 'hufflepuff': 1}),
          Answer(text: "Mangemort", scores: {'dark_wizard': 4}),
        ],
      ),
      // Question 18
      Question(
        text: "Vous trouvez un Horcruxe. Que faites-vous ?",
        answers: [
          Answer(text: "Je le détruis immédiatement", scores: {'gryffindor': 3, 'auror': 3}),
          Answer(text: "J'étudie son pouvoir", scores: {'dark_wizard': 3, 'slytherin': 2}),
          Answer(text: "Je cherche comment le détruire en toute sécurité", scores: {'ravenclaw': 3}),
          Answer(text: "J'alerte les autorités magiques", scores: {'hufflepuff': 3, 'auror': 1}),
        ],
      ),
      // Question 19
      Question(
        text: "Votre devise personnelle serait...",
        answers: [
          Answer(text: "Fortune favors the brave", scores: {'gryffindor': 3}),
          Answer(text: "Power is everything", scores: {'slytherin': 2, 'dark_wizard': 3}),
          Answer(text: "Knowledge is power", scores: {'ravenclaw': 3}),
          Answer(text: "Together we are stronger", scores: {'hufflepuff': 3}),
        ],
      ),
      // Question 20
      Question(
        text: "Si vous pouviez changer le monde magique, vous...",
        answers: [
          Answer(text: "Le rendrais plus juste et égalitaire", scores: {'gryffindor': 2, 'hufflepuff': 3}),
          Answer(text: "Prendriez le pouvoir pour le diriger", scores: {'slytherin': 3, 'dark_wizard': 2}),
          Answer(text: "Créeriez plus d'écoles et de savoirs", scores: {'ravenclaw': 3}),
          Answer(text: "Protégeriez toutes les créatures magiques", scores: {'hufflepuff': 3}),
        ],
      ),
    ];
  }
}
