import factory

from eums.models import NumericQuestion, MultipleChoiceQuestion, TextQuestion


class NumericQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = NumericQuestion

    text = 'How old are you?'
    label = factory.Sequence(lambda n: 'numeric_label {0}'.format(n))
    uuids = [factory.Sequence(lambda n: '{0}'.format(n))]


class TextQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = TextQuestion

    text = 'What is your name'
    label = factory.Sequence(lambda n: 'text_label {0}'.format(n))
    uuids = [factory.Sequence(lambda n: '{0}'.format(n))]


class MultipleChoiceQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = MultipleChoiceQuestion

    text = 'What is your name'
    label = factory.Sequence(lambda n: 'multiple_choice_label {0}'.format(n))
    uuids = [factory.Sequence(lambda n: '{0}'.format(n))]