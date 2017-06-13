"""
Conversion tools
"""

import os
from corpkit.constants import OPENER


def make_file_or_df(data, xml, make_file, corpus_name=False):
    """
    Either make a file with .conll on the end, or return a pd.DataFrame
    """
    if make_file:
        outname = xml + '.conll'
        with OPENER(outname, 'w') as fo:
            fo.write(data)
        return
    else:
        from corpkit.conll import parse_conll
        return parse_conll(data,
                           with_meta=False,
                           usecols=None,
                           io=os.path.splitext(xml)[0],
                           corpus_name=corpus_name,
                           corp_folder="todo")

def srt_to_corpkit(srt, enc="utf-8", extra_metadata={}):
    """
    Take an SRT subtitle file and convert it to something corpkit can parse.
    A file is created in the same directory, with a .txt extension.

    This is a proof of concept in a multimodal analysis workflow.

    Args:
        srt (str): path to .srt file
    """
    import re
    from collections import defaultdict
    
    # so we can pass in an srt string (for youtube videos)
    if os.path.isfile(srt):
        extra_metadata['file'] = srt
        end_or_dur = 'end'
        with OPENER(srt, 'r', encoding=enc) as fo:    
            data = fo.read()
    else:
        end_or_dur = 'dur'
        data = srt
        srt = extra_metadata.pop('outpath')
    data = data.split('\n\n')
    out = []
    sents = defaultdict(list)
    sent_count = 0
    for caption in data:
        i, time, *text = caption.splitlines()
        time = time.strip()
        text = ' '.join(text)
        # yeah, this parses xml as a regex, so what?
        text = re.sub('<[^<]+?>', '', text)
        #tree = ET.fromstring(text)
        #text = ET.tostring(tree, encoding='utf8', method='text').strip().decode()
        sents[sent_count].append((text, time))
        if text.endswith('.'):
            sent_count += 1

    for n, sent in sorted(sents.items()):
        to_be_string = []
        for i, (text, time) in enumerate(sent):
            if i == 0:
                extra_metadata['start'] = time.split(' ')[0]
            if i == len(sent)-1:
                extra_metadata[end_or_dur] = time.split(' ')[-1]
            to_be_string.append(text)
        sent_string = ' '.join(to_be_string)
        metadata = ' <metadata'
        for k, v in extra_metadata.items():
            metadata += ' %s="%s"' % (str(k), str(v))
        metadata += '>'
        sent_string += metadata
        out.append(sent_string)
    outname = os.path.splitext(srt)[0] + '.txt'
    with OPENER(outname, 'w') as fo:
        fo.write('\n'.join(out))
    return outname

def tundra_to_corpkit(xml, mode='dependency', make_file=True, corpus_name=False):
    """
    Take a TüNDRA XML format file and turn it into conll-u/corpkit parsed format
    """
    from lxml import etree
    tree = etree.parse(xml)
    out = []
    if mode.startswith('d'):
        for sent in list(tree.getroot()):
            sent_str = []
            sent_data = {}
            # cons is a dummy, the root of the dep parse
            root = sent[0]
            # in xml the numbers just keep incrementing, so we will subtract the
            # root number from every token
            start_at = int(root.get('num', 0))

            # ignore nesting, just get every token element
            for token in root.iterfind('.//token'):
                # get its corpkit index
                i = int(token.get('order')) - start_at
                # governor id is parent's "order" attr, minus start_at
                gov_id = int(token.getparent().get('order', 0))
                if gov_id:
                    gov_id -= start_at
                # deps are any immediate child nodes
                deps = token.findall('token')
                # format them
                depnums = [str(int(x.get('order')) - start_at) for x in deps]
                deps = ','.join(depnums)
                # make our token line
                line = [i,
                        token.get('token', '_'),
                        token.get('lemma', '_'),
                        token.get('pos', '_'),
                        token.get('ner', '_'),
                        token.get('morph', '_'),
                        token.get('edge', '_'),
                        deps,
                        '_' ]
                sent_data[i] = line
            for i, line in sorted(list(sent_data.items())):
                form = '\t'.join([str(i)] + line)
                sent_str.append(form)
            out.append('\n'.join(sent_str) + '\n')
    else:
        raise NotImplementedError
    out = '\n'.join(out)
    return make_file_or_df(out, xml, make_file, corpus_name)

def tcf_to_corpkit(tcf, mode='dependency', make_file=True, corpus_name=False):
    """
    Take a tcf format file and turn it into conll-u/corpkit parsed format
    """
    from lxml import etree
    from corpkit.conll import parse_conll
    tree = etree.parse(tcf)
    out = []
    root = tree.getroot()
    corpus = root[-1]
    coref_dict = {}
    coref_num = 1
    # the particular layers are not in set order and may not be there,
    # so this is wrong. need to recognise them from their names instead
    _, tokens, sentences, lemmas, postags, depparsing, ner, coref = list(corpus)
    for sent in sentences:
        toks = sent.get('tokenIDs').split()
        for i, tok_id in enumerate(toks, start=1):
            m = "_"
            w = tokens[i-1].text
            l = lemmas[i-1].text
            p = postags[i-1].text
            e = ner.xpath("//*[local-name() = 'entity']")
            e = next((x.get('class') for x in e if x.get('tokenIDs') == tok_id), '_')
            dep = depparsing.xpath("//*[local-name() = 'dependency']")
            # definitely the worst line i've ever written, but it's nice and fast
            g, f = next(((str(toks.index(x.get('govIDs'))+1), x.get('func')) \
                        for x in dep if x.get('depIDs') == tok_id), ('_', '_'))
            d = [str(toks.index(x.get('depIDs'))+1) for x in dep if x.get('govIDs') == tok_id]
            if d:
                d = ','.join(d)
            else:
                d = '_'
            # last, hardest bit: corefs
            # get every reference
            c = coref.xpath("//*[local-name() = 'reference']")
            # get the entity for the first match

            parent = next((x.getparent() for x in c if x.get("tokenIDs") == tok_id), '_')
            # if the token exists within a coref chain
            if parent != '_':
                # try to get the number of this parent from storage
                # if it doesn't exist yet, create it and increment the number
                try:
                    num = coref_dict[parent]
                    c = str(num) + '*'
                except KeyError:
                    coref_dict[parent] = coref_num
                    c = str(coref_num) + '*'
                    coref_num += 1
            else:
                c = parent
            
            line = '\t'.join([str(i), w, l, p, e, m, g, f, d, c])
            out.append(line)
        out.append('\n')
    out = '\n'.join(out)
    return make_file_or_df(out, tcf, make_file, corpus_name)


def formatSrtTime(secTime):
    """Convert a time in seconds (google's transcript) to srt time format."""
    sec, micro = str(secTime).split('.')
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h,m,s,micro)

def make_srt_line(i, line):
    form_text = line.text.strip().replace('\n', ' ')
    tup = (i, line.get('start'), line.get('dur'), form_text)
    return '%d\n%s --> %s\n%s' % tup

def youtube_to_corpkit(id_string, outpath=False, lang="en"):
    """
    Download captions for a YouTube video and convert to corpkit unparsed
    
    Args:
        id_string (str): a YouTube video ID, e.g. 'FfOTmfwRTFs'
        outpath (str): where to save the file. defaults to ./id_string.txt
        lang (str): two character language code

    Returns:
        str: path to created file
    """
    import requests
    from lxml import etree
    try:
        import HTMLParser
        pars = HTMLParser.HTMLParser()
    except ImportError:
        from html.parser import HTMLParser
        pars = HTMLParser()

    # if the user gives a youtube link
    video_url = False
    if 'youtube' in id_string:
        video_url = str(id_string)
        id_string = id_string.split('=')[-1]
    
    lang_trans = {'english': 'en', 'german': 'de'}

    if len(lang) != 2:
        lang = lang_trans.get(lang.lower(), lang[:2].lower())

    if not video_url:
        video_url = "https://www.youtube.com/watch?v=" + id_string

    text_url = 'http://video.google.com/timedtext?lang=%s&v=%s' % (lang, id_string)
    xml = requests.get(text_url).content
    root = etree.fromstring(xml)
    out = []
    for i, line in enumerate(root, start=1):
        form_text = pars.unescape(line.text.strip().replace('\n', ' '))
        tup = (i, line.get('start'), line.get('dur'), form_text)
        out.append('%d\n%s --> %s\n%s' % tup)
    out = '\n\n'.join(out)


    if not outpath:
        the_outpath = id_string + '.txt'
    elif outpath.endswith('.txt'):
        the_outpath = outpath
    else:
        the_outpath = os.path.join(outpath, id_string + '.txt')

    extra_metadata = {'text_url': text_url,
                      'video_url': video_url,
                      'type': 'youtube',
                      'outpath': the_outpath,
                      'id_string': id_string}
    return srt_to_corpkit(out, extra_metadata=extra_metadata)
