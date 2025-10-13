class WizardType {
  final String id;
  final String name;
  final String description;
  final String characteristics;
  final String famousWizards;
  final String houseColors;
  final String emoji;

  WizardType({
    required this.id,
    required this.name,
    required this.description,
    required this.characteristics,
    required this.famousWizards,
    required this.houseColors,
    required this.emoji,
  });
}

class WizardTypes {
  static final gryffindor = WizardType(
    id: 'gryffindor',
    name: 'Sorcier de Gryffondor',
    description: 'Courageux, audacieux et chevaleresque',
    characteristics: 'Vous êtes brave, déterminé et prêt à défendre vos amis. Vous n\'hésitez pas à prendre des risques pour faire ce qui est juste.',
    famousWizards: 'Harry Potter, Hermione Granger, Albus Dumbledore',
    houseColors: '🔴 Rouge et Or',
    emoji: '🦁',
  );

  static final slytherin = WizardType(
    id: 'slytherin',
    name: 'Sorcier de Serpentard',
    description: 'Ambitieux, rusé et déterminé',
    characteristics: 'Vous êtes stratégique, ambitieux et savez comment atteindre vos objectifs. Vous utilisez votre intelligence pour réussir.',
    famousWizards: 'Severus Rogue, Merlin, Horace Slughorn',
    houseColors: '🟢 Vert et Argent',
    emoji: '🐍',
  );

  static final ravenclaw = WizardType(
    id: 'ravenclaw',
    name: 'Sorcier de Serdaigle',
    description: 'Intelligent, sage et créatif',
    characteristics: 'Vous valorisez la connaissance et la sagesse. Votre curiosité intellectuelle et votre créativité vous distinguent.',
    famousWizards: 'Luna Lovegood, Cho Chang, Filius Flitwick',
    houseColors: '🔵 Bleu et Bronze',
    emoji: '🦅',
  );

  static final hufflepuff = WizardType(
    id: 'hufflepuff',
    name: 'Sorcier de Poufsouffle',
    description: 'Loyal, travailleur et juste',
    characteristics: 'Vous êtes loyal, patient et juste. Vous valorisez le travail acharné et l\'équité pour tous.',
    famousWizards: 'Newt Scamander, Cedric Diggory, Nymphadora Tonks',
    houseColors: '🟡 Jaune et Noir',
    emoji: '🦡',
  );

  static final auror = WizardType(
    id: 'auror',
    name: 'Auror',
    description: 'Protecteur du monde magique',
    characteristics: 'Vous êtes un défenseur de la justice magique. Combattre les forces du mal est votre vocation.',
    famousWizards: 'Alastor Maugrey, Nymphadora Tonks, Harry Potter',
    houseColors: '⚫ Noir et Bleu',
    emoji: '⚡',
  );

  static final darkWizard = WizardType(
    id: 'dark_wizard',
    name: 'Mage Noir',
    description: 'Puissant et mystérieux',
    characteristics: 'Vous êtes attiré par la magie noire et le pouvoir absolu. Votre ambition n\'a pas de limites.',
    famousWizards: 'Voldemort, Gellert Grindelwald, Bellatrix Lestrange',
    houseColors: '⚫ Noir et Vert',
    emoji: '💀',
  );

  static List<WizardType> getAllTypes() {
    return [gryffindor, slytherin, ravenclaw, hufflepuff, auror, darkWizard];
  }
}
