from knights import render


class TestHelpers:
    def test_escape_html(self):
        result = render("""{{ _.escape("foo & bar") }}""")
        assert result == 'foo &amp; bar'

    def test_escape_js(self):
        result = render("""{{ _.escape('=', 'js') }}""")
        assert result == '\\u003D'

    def test_add_slashes(self):
        result = render("""{{ _.addslashes(val) }}""", {'val': r'\test'})
        assert result ==  r"\\test"
    
    def test_capfirst(self):
        result = render('{{ _.capfirst(name) }}', {'name': 'bob down'})
        assert result == 'Bob down'