from ibl_stuff import api


def test_load():
    api.init_host()
    assert "base" in api.__name__

    api.init_host("maya")
    assert "maya" in api.__name__

    api.init_host("nuke")
    assert "nuke" in api.__name__
