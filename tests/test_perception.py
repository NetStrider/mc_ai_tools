from mcai_agent.perception import parse_chat


def test_parse_chat():
    line = "[13:23:01] [Server thread/INFO]: <Steve> hello world"
    r = parse_chat(line)
    assert r == ("Steve", "hello world")
