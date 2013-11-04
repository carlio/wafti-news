import sys
from lettuce import step, world
from hamcrest import *
from django.contrib.markup.templatetags import markup
from lxml import html
from formencode.doctest_xml_compare import xml_compare


@step(u'Then I see the header "([^"]*)"')
def see_header(step, text):
    assert world.browser.is_text_present(text)


@step(u'Then I see the headline "([^"]*)"')
def see_headline(step, text):
    assert world.browser.is_text_present(text)


@step(u'Then I see the content')
def then_i_see_the_content(step):

    expected = html.fromstring(
        '<div property="<http://schema.org/text>">%s</div>' % markup.markdown(world.content))

    actual = html.fromstring(
        world.browser.find_by_css('article div').outer_html)

    reporter = lambda x: sys.stdout.write(x + "\n")
    assert xml_compare(expected, actual, reporter)


@step(u'Then the headline should be "([^"]*)"')
def then_the_headline_should_be(step, headline):
    assert_that(world.browser.find_by_css('article h2').first.text, is_(headline))


@step(u'Then the headline should still be "([^"]*)"')
def then_the_headline_should_still_be(step, headline):
    step.then('Then the headline should be "{}"'.format(headline))


@step(u'Then the first headline should be "([^"]*)"')
def check_first_headline(step, headline):
    assert_that(world.browser.find_by_css('h2').first.text, is_(headline))
