import sys
import os
sys.path.append('../org_to_anki')

# Anki deck
from org_to_anki.ankiClasses.AnkiDeck import AnkiDeck
from org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion

def testGettingDeckNames():

    # Create deck with subdeck
    parent = AnkiDeck("parent")
    child = AnkiDeck("child")
    subChild = AnkiDeck("subChild")

    child.addSubdeck(subChild)
    parent.addSubdeck(child)

    deckNames = parent.getDeckNames()

    assert(deckNames == ["parent", "parent::child", "parent::child::subChild"])

def testDeckNameSetFor_GetAllDeckQuestion():

    parent = AnkiDeck("parent")
    child = AnkiDeck("child")
    subChild = AnkiDeck("subChild")

    child.addSubdeck(subChild)
    parent.addSubdeck(child)

    # Expected question
    expectedQuestion1 = AnkiQuestion("What is the capital of Ireland")
    expectedQuestion1.addAnswer("Dublin")
    expectedQuestion1.setDeckName("parent")

    expectedQuestion2 = AnkiQuestion("What is the capital of France")
    expectedQuestion2.addAnswer("Paris")
    expectedQuestion2.setDeckName("parent::child")

    expectedQuestion3 = AnkiQuestion("What is the capital of Germany")
    expectedQuestion3.addAnswer("Berlin")
    expectedQuestion3.setDeckName("parent::child::subChild")

    # Add questions
    firstQuestion = AnkiQuestion("What is the capital of Ireland")
    firstQuestion.addAnswer("Dublin")
    parent.addQuestion(firstQuestion)

    secondQuestion = AnkiQuestion("What is the capital of France")
    secondQuestion.addAnswer("Paris")
    child.addQuestion(secondQuestion)

    thirdQuestion = AnkiQuestion("What is the capital of Germany")
    thirdQuestion.addAnswer("Berlin")
    subChild.addQuestion(thirdQuestion)

    # Comprae
    questions = parent.getQuestions()

    assert(questions == [expectedQuestion1, expectedQuestion2, expectedQuestion3])


def testCommentsAndParametersForAnkiQuestion():

    q = AnkiQuestion("Test question")
    q.addAnswer("Test Answer")
    q.addTag("test tag")
    q.addComment("Test comment")
    q.addParameter("type", "basic")
    q.addParameter("type1", "basic1")

    assert(q.getAnswers() == ["Test Answer"])
    assert(q.getTags() == ["test tag"])
    assert(q.getComments() == ["Test comment"])
    assert(q.getParameter("type") == "basic")
    assert(q.getParameter("type1") == "basic1")
    assert(q.getParameter("notFound") == None)


def testQuestionInheritParamsFromDeck():


    q1 = AnkiQuestion("Test question")
    q1.addAnswer("Test Answer")
    q1.addParameter("type", "reversed")

    deck = AnkiDeck("Test Deck")
    deck.addParameter("type1", "basic1")
    deck.addParameter("type", "basic")
    deck.addQuestion(q1)

    questions = deck.getQuestions()

    assert(questions[0].getParameter("type") == "reversed")
    assert(questions[0].getParameter("type1") == "basic1")

def testDecksInheritParamsFromParentDeck():

    q1 = AnkiQuestion("Test question")
    q1.addAnswer("Test Answer")
    q1.addParameter("q0", "question")

    deck0 = AnkiDeck("deck0")
    deck0.addParameter("deck0", "deck0")
    deck0.addQuestion(q1)

    deck1 = AnkiDeck("deck1")
    deck1.addParameter("deck1", "deck1")
    deck1.addSubdeck(deck0)

    deck2 = AnkiDeck("deck2")
    deck2.addParameter("deck2", "deck2")
    deck2.addParameter("deck1", "deck2")
    deck2.addParameter("deck0", "deck2")
    deck2.addParameter("q0", "deck2")
    deck2.addSubdeck(deck1)

    questions = deck2.getQuestions()
    print(deck2._parameters)

    print(questions[0]._parameters)
    assert(questions[0].getParameter("deck2") == "deck2")
    assert(questions[0].getParameter("deck1") == "deck1")
    assert(questions[0].getParameter("deck0") == "deck0")
    assert(questions[0].getParameter("q0") == "question")
