class TestInheritance:
    def test_simple(self, test_loader):
        """
        Test that we can inherit.
        """
        t = test_loader.load('inherit_simple.html')
        result = t({})
        assert result == 'parent\n\n'

    def test_override_block(self, test_loader):
        t = test_loader.load('inherit_override.html')
        result = t({})
        assert result == 'parent\nchild\n'


class TestSuper:
    def test_own_super(self, test_loader):
        t = test_loader.load('super_own.html')
        result = t({})
        assert result == 'child of parent\nother parent\n'

    def test_other_super(self, test_loader):
        t = test_loader.load('super_other.html')
        result = t({})
        assert result == 'subverting other parent\nother parent\n'
