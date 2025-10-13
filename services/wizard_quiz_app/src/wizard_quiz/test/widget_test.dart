import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:wizard_quiz/main.dart';
import 'package:wizard_quiz/models/wizard_type.dart';
import 'package:wizard_quiz/utils/quiz_data.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const WizardQuizApp());

    // Verify that the welcome screen loads
    expect(find.text('TU ES UN SORCIER,'), findsOneWidget);
    expect(find.text('HARRY !'), findsOneWidget);
  });

  test('WizardTypes has 6 types', () {
    final types = WizardTypes.getAllTypes();
    expect(types.length, 6);
  });

  test('Quiz has 20 questions', () {
    final questions = QuizData.getQuestions();
    expect(questions.length, 20);
  });

  test('Each question has 4 answers', () {
    final questions = QuizData.getQuestions();
    for (var question in questions) {
      expect(question.answers.length, 4);
    }
  });

  test('Wizard types have correct IDs', () {
    final types = WizardTypes.getAllTypes();
    final ids = types.map((t) => t.id).toList();
    
    expect(ids.contains('gryffindor'), true);
    expect(ids.contains('slytherin'), true);
    expect(ids.contains('ravenclaw'), true);
    expect(ids.contains('hufflepuff'), true);
    expect(ids.contains('auror'), true);
    expect(ids.contains('dark_wizard'), true);
  });
}
