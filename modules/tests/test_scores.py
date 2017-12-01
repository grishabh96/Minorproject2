import modules


def test_scores():
    assert ('news' == modules.process_query('scores')[0])
    assert ('news' == modules.process_query('latest scores')[0])
    assert ('news' == modules.process_query('world scores')[0])
    assert ('news' != modules.process_query('something random score')[0])
