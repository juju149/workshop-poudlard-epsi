import 'package:flutter/material.dart';
import '../models/wizard_type.dart';
import 'welcome_screen.dart';

class ResultScreen extends StatelessWidget {
  final Map<String, int> scores;

  const ResultScreen({super.key, required this.scores});

  WizardType _determineWizardType() {
    // Find the wizard type with the highest score
    String highestScoringType = scores.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;

    // Get the corresponding WizardType
    return WizardTypes.getAllTypes()
        .firstWhere((type) => type.id == highestScoringType);
  }

  Color _getThemeColor(String wizardId) {
    switch (wizardId) {
      case 'gryffindor':
        return const Color(0xFFae0001);
      case 'slytherin':
        return const Color(0xFF1a472a);
      case 'ravenclaw':
        return const Color(0xFF0e1a40);
      case 'hufflepuff':
        return const Color(0xFFecb939);
      case 'auror':
        return const Color(0xFF2c3e50);
      case 'dark_wizard':
        return const Color(0xFF1a1a1a);
      default:
        return const Color(0xFF1a1a2e);
    }
  }

  @override
  Widget build(BuildContext context) {
    final wizardType = _determineWizardType();
    final themeColor = _getThemeColor(wizardType.id);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              themeColor,
              themeColor.withOpacity(0.7),
              const Color(0xFF1a1a2e),
            ],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                children: [
                  const SizedBox(height: 20),
                  
                  // Confetti or celebration
                  const Text(
                    '✨ 🎉 ✨',
                    style: TextStyle(fontSize: 50),
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // "You are" text
                  const Text(
                    'Tu es un...',
                    style: TextStyle(
                      fontSize: 24,
                      color: Colors.white70,
                      fontWeight: FontWeight.w500,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  const SizedBox(height: 16),
                  
                  // Wizard type emoji
                  Text(
                    wizardType.emoji,
                    style: const TextStyle(fontSize: 100),
                  ),
                  
                  const SizedBox(height: 16),
                  
                  // Wizard type name
                  Text(
                    wizardType.name,
                    style: const TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  const SizedBox(height: 12),
                  
                  // House colors
                  Text(
                    wizardType.houseColors,
                    style: const TextStyle(
                      fontSize: 18,
                      color: Colors.white70,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  
                  const SizedBox(height: 32),
                  
                  // Description card
                  Card(
                    color: Colors.white.withOpacity(0.15),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '📜 Description',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            wizardType.description,
                            style: const TextStyle(
                              fontSize: 16,
                              color: Colors.white,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            wizardType.characteristics,
                            style: const TextStyle(
                              fontSize: 15,
                              color: Colors.white70,
                              height: 1.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // Famous wizards card
                  Card(
                    color: Colors.white.withOpacity(0.15),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '⭐ Sorciers célèbres',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            wizardType.famousWizards,
                            style: const TextStyle(
                              fontSize: 15,
                              color: Colors.white70,
                              height: 1.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // Score breakdown
                  Card(
                    color: Colors.white.withOpacity(0.15),
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            '📊 Détail des scores',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 16),
                          ...scores.entries.map((entry) {
                            final percentage = (entry.value / scores.values.reduce((a, b) => a + b) * 100).toInt();
                            return Padding(
                              padding: const EdgeInsets.symmetric(vertical: 4.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        _getWizardName(entry.key),
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontSize: 14,
                                        ),
                                      ),
                                      Text(
                                        '${entry.value} pts ($percentage%)',
                                        style: const TextStyle(
                                          color: Colors.white70,
                                          fontSize: 14,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 4),
                                  ClipRRect(
                                    borderRadius: BorderRadius.circular(4),
                                    child: LinearProgressIndicator(
                                      value: percentage / 100,
                                      backgroundColor: Colors.white.withOpacity(0.2),
                                      valueColor: AlwaysStoppedAnimation<Color>(
                                        _getWizardColor(entry.key),
                                      ),
                                      minHeight: 8,
                                    ),
                                  ),
                                ],
                              ),
                            );
                          }).toList(),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  
                  // Restart button
                  ElevatedButton(
                    onPressed: () {
                      Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const WelcomeScreen(),
                        ),
                        (route) => false,
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFe94560),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 48,
                        vertical: 20,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const [
                        Icon(Icons.refresh),
                        SizedBox(width: 12),
                        Text(
                          'RECOMMENCER',
                          style: TextStyle(fontSize: 18),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  String _getWizardName(String id) {
    switch (id) {
      case 'gryffindor':
        return '🦁 Gryffondor';
      case 'slytherin':
        return '🐍 Serpentard';
      case 'ravenclaw':
        return '🦅 Serdaigle';
      case 'hufflepuff':
        return '🦡 Poufsouffle';
      case 'auror':
        return '⚡ Auror';
      case 'dark_wizard':
        return '💀 Mage Noir';
      default:
        return id;
    }
  }

  Color _getWizardColor(String id) {
    switch (id) {
      case 'gryffindor':
        return const Color(0xFFae0001);
      case 'slytherin':
        return const Color(0xFF1a472a);
      case 'ravenclaw':
        return const Color(0xFF0e1a40);
      case 'hufflepuff':
        return const Color(0xFFecb939);
      case 'auror':
        return const Color(0xFF2c3e50);
      case 'dark_wizard':
        return const Color(0xFF1a1a1a);
      default:
        return Colors.grey;
    }
  }
}
