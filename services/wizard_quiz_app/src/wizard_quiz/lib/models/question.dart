class Question {
  final String text;
  final List<Answer> answers;

  Question({required this.text, required this.answers});
}

class Answer {
  final String text;
  final Map<String, int> scores;

  Answer({required this.text, required this.scores});
}
