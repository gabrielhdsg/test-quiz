import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# commit 2: 10 unit tests
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q2', points=101)


def test_remove_choice_by_id_removes_only_that_choice():
    question = Question(title='q5')
    c1 = question.add_choice('a', False)
    c2 = question.add_choice('b', False)

    question.remove_choice_by_id(c1.id)

    remaining_ids = []
    for choice in question.choices:
        remaining_ids.append(choice.id)
    assert remaining_ids == [c2.id]

def test_add_multiple__incremental_ids():
    question = Question(title='q10')
    first = question.add_choice('a', False)
    second = question.add_choice('b', True)

    assert first.id == 1
    assert second.id == 2
    assert second.id == first.id + 1

def test_remove_choice_by_id_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a', False)

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_choices():
    question = Question(title='q8')
    question.add_choice('a', False)
    question.add_choice('b', False)
    question.add_choice('c', True)

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_set_correct_choices_marks_corrects_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a', False)
    c2 = question.add_choice('b', False)
    c3 = question.add_choice('c', False)

    question.set_correct_choices([c1.id, c3.id])

    assert c1.is_correct
    assert not c2.is_correct
    assert c3.is_correct


def test_set_correct_choices_with_invalid_id():
    question = Question(title='q1')
    question.add_choice('a', False)

    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_returns_only_correct_ids():
    question = Question(title='q1', max_selections=4)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)
    c3 = question.add_choice('c', True)
    c4 = question.add_choice('d', False)

    result = question.correct_selected_choices([c1.id, c2.id, c3.id, c4.id])

    assert set(result) == {c1.id, c3.id}


def test_correct_selected_choices_respects_max_selections():
    question = Question(title='q2', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', False)

    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])


def test_add_choice_validates_constraints():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('', False)

    with pytest.raises(Exception):
        question.add_choice('a' * 101, False)

# commit 3: 2 unit tests
@pytest.fixture
def question_with_choices():
    """
    Questão com múltiplas alternativas
    """
    question = Question(title='Questão do Commit 3', max_selections=3)
    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)
    return question, [choice1, choice2, choice3]

def test_correct_selected_choices(question_with_choices):
    question, choices = question_with_choices

    selected_ids = []
    for choice in choices:
        selected_ids.append(choice.id)

    result = question.correct_selected_choices(selected_ids)

    expected_ids = [choices[0].id, choices[2].id]
    assert list(result) == expected_ids


def test_remove_all_choices(question_with_choices):
    question, dump = question_with_choices

    question.remove_all_choices()

    assert len(question.choices) == 0