import io
import syntacticalAnalyzer


def test_one_simple_file(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_simple_files(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a.txt').write_text('hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'b.txt').write_text('_hASDasdellfoasf :- fasd; g_as; fAD, _g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt: Correct\n' \
                  'b.txt: Correct\n'


def test_line(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO('_hASDasdellfoasf :- a. asdas:- ((((asd)))).'))
    syntacticalAnalyzer.main([])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_multi_line(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDasdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea'
        ':- aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea,\n\n\n\n\n sad\n\n\n'
        ',\n\n\n\n\n (\n\n\n\n asd;\n\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main([])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Correct\n'


def test_error_line_lex(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDa/sdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'asdafdscjhbea'
        ':- aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea,\n\n\n\n\n sad\n\n\n'
        ',\n\n\n\n\n (\n\n\n\n asd;\n\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main([])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'IllegalCharacter: \'/\', line 40\n'


def test_error_line_par(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        '_hASDasdellfoasf :- a.\n'
        'asd\n :-\n asd, \n\n\n sa\n\n\n\n.'
        'asdafdscjhbea'
        ':- aasdaSALKJFDNAFKLAjdsljdsajflkKJBFKJQWNfdsfhldsajfhkjsdhfkjdhfkjdshfkjehkjskdbcjhbea\n\n\n\n\n sad\n\n\n'
        ',\n\n\n\n\n (\n\n\n\n asd;\n\n\n asd\n\n\n)\n\n\n.'))
    syntacticalAnalyzer.main([])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'IncompleteToken: at line 51\n'


def test_error_files(monkeypatch, tmp_path, capsys):
    (tmp_path / 'a').write_text('hello :- f; g; f, g, f, g, (((((f)), ((g, ggg)), g, ggg, fgfgfg, fg))).\n')
    (tmp_path / 'b').write_text('hello :- (f; g)); f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'c').write_text('Ahello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'd').write_text('9hello :- f; g; f, g, f, g, f, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'e').write_text('hello :- f; g; f, g, f, g, f\\, g, ggg, g, ggg, fgfgfg, fg.\n')
    (tmp_path / 'f').write_text('hello :- f; g; (f, g, f, g, f,) g, ggg, g, ggg, fgfgfg, fg.\n')

    monkeypatch.chdir(tmp_path)
    syntacticalAnalyzer.main(['a', 'b', 'c', 'd', 'e', 'f'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a: Correct\n' \
                  'b: IncompleteToken: at line 78\n' \
                  'c: Correct\n' \
                  'd: IllegalCharacter: \'9\', line 79\n' \
                  'e: IllegalCharacter: \'\\\', line 79\n' \
                  'f: IncompleteToken: at line 80\n'
