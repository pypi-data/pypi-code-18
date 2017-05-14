# -*- coding: utf-8 -*-

# Functions for all standard HTML tags
# Documentation included from the Mozilla Developer Network website
# https://developer.mozilla.org/en-US/docs/Web/HTML/Element

from .core import el, void_el


# Main root
def html(*args, **kwargs):
    """
    The HTML <html> element (or HTML root element) represents the root
    of an HTML document. All other elements must be descendants of
    this element.
    """
    return el('html', *args, **kwargs)


# Document metadata
def base(*args, **kwargs):
    """
    The HTML <base> element specifies the base URL to use for all
    relative URLs contained within a document. There can be only one
    <base> element in a document.
    """
    return void_el('base', *args, **kwargs)


def head(*args, **kwargs):
    """
    The HTML <head> element provides general information (metadata)
    about the document, including its title and links to its scripts
    and style sheets.
    """
    return el('head', *args, **kwargs)


def link(*args, **kwargs):
    """
    The HTML <link> element specifies relationships between the
    current document and an external resource. Possible uses for this
    element include defining a relational framework for
    navigation. This Element is most used to link to style sheets.
    """
    return void_el('link', *args, **kwargs)


def meta(*args, **kwargs):
    """
    The HTML <meta> element represents any metadata information that
    cannot be represented by one of the other HTML meta-related
    elements (<base>, <link>, <script>, <style> or <title>).
    """
    return void_el('meta', *args, **kwargs)


def style(*args, **kwargs):
    """
    The HTML <style> element contains style information for a
    document, or part of a document. By default, the style
    instructions written inside that element are expected to be CSS.
    """
    return el('style', *args, **kwargs)


def title(*args, **kwargs):
    """
    The HTML <title> element defines the title of the document, shown
    in a browser's title bar or on the page's tab. It can only contain
    text, and any contained tags are ignored.
    """
    return el('title', *args, **kwargs)


# Content sectioning

def body(*args, **kwargs):
    """
    The HTML <body> Element represents the content of an HTML
    document. There can be only one <body> element in a document.
    """
    return el('body', *args, **kwargs)


def address(*args, **kwargs):
    """
    The HTML <address> element supplies contact information for its
    nearest <article> or <body> ancestor; in the latter case, it
    applies to the whole document.
    """
    return el('address', *args, **kwargs)


def article(*args, **kwargs):
    """
    The HTML <article> element represents a self-contained composition
    in a document, page, application, or site, which is intended to be
    independently distributable or reusable (e.g., in
    syndication). This could be a forum post, a magazine or newspaper
    article, a blog entry, an object, or any other independent item of
    content. Each <article> should be identified, typically by
    including a heading (<h1>-<h6> element) as a child of the
    <article> element.
    """
    return el('article', *args, **kwargs)


def aside(*args, **kwargs):
    """
    The HTML <aside> element represents a section of the page with
    content connected tangentially to the rest, which could be
    considered separate from that content. These sections are often
    represented as sidebars or inserts. They often contain the
    definitions on the sidebars, such as definitions from the
    glossary; there may also be other types of information, such as
    related advertisements; the biography of the author; web
    applications; profile information or related links on the blog.
    """
    return el('aside', *args, **kwargs)


def footer(*args, **kwargs):
    """
    The HTML <footer> element represents a footer for its nearest
    sectioning content or sectioning root element. A footer typically
    contains information about the author of the section, copyright
    data or links to related documents.
    """
    return el('footer', *args, **kwargs)


def header(*args, **kwargs):
    """
    The HTML <header> element represents a group of introductory or
    navigational aids. It may contain some heading elements but also
    other elements like a logo, wrapped section's header, a search
    form, and so on.
    """
    return el('header', *args, **kwargs)


def h1(*args, **kwargs):
    """
    Heading elements implement six levels of document
    headings, < h1 > is the most important and < h6 > is the
    least. A heading element briefly describes the topic of
    the section it introduces. Heading information may be used
    by user agents, for example, to construct a table of
    contents for a document automatically.
    """
    return el('h1', *args, **kwargs)


def h2(*args, **kwargs):
    """
    Heading elements implement six levels of document
    headings, < h1 > is the most important and < h6 > is the
    least. A heading element briefly describes the topic of
    the section it introduces. Heading information may be used
    by user agents, for example, to construct a table of
    contents for a document automatically.
    """
    return el('h2', *args, **kwargs)


def h3(*args, **kwargs):
    """
    Heading elements implement six levels of document
    headings, < h1 > is the most important and < h6 > is the
    least. A heading element briefly describes the topic of
    the section it introduces. Heading information may be used
    by user agents, for example, to construct a table of
    contents for a document automatically.
    """
    return el('h3', *args, **kwargs)


def h4(*args, **kwargs):
    """
    Heading elements implement six levels of document
    headings, < h1 > is the most important and < h6 > is the
    least. A heading element briefly describes the topic of
    the section it introduces. Heading information may be used
    by user agents, for example, to construct a table of
    contents for a document automatically.
    """
    return el('h4', *args, **kwargs)


def h5(*args, **kwargs):
    """
    Heading elements implement six levels of document headings, < h1 >
    is the most important and < h6 > is the least. A heading element
    briefly describes the topic of the section it introduces. Heading
    information may be used by user agents, for example, to construct
    a table of contents for a document automatically.
    """
    return el('h5', *args, **kwargs)


def h6(*args, **kwargs):
    """
    Heading elements implement six levels of document headings, < h1 >
    is the most important and < h6 > is the least. A heading element
    briefly describes the topic of the section it introduces. Heading
    information may be used by user agents, for example, to construct
    a table of contents for a document automatically.
    """
    return el('h6', *args, **kwargs)


def hgroup(*args, **kwargs):
    """
    The HTML <hgroup> Element (HTML Heading Group Element) represents
    the heading of a section. It defines a single title that
    participates in the outline of the document as the heading of the
    implicit or explicit section that it belongs to.
    """
    return el('hgroup', *args, **kwargs)


def nav(*args, **kwargs):
    """
    The HTML <nav> element (HTML Navigation Element) represents a
    section of a page that links to other pages or to parts within the
    page: a section with navigation links.
    """
    return el('nav', *args, **kwargs)


def section(*args, **kwargs):
    """
    The HTML <section> element represents a generic section of a
    document, i.e., a thematic grouping of content, typically with a
    heading. Each <section> should be identified, typically by
    including a heading (<h1>-<h6> element) as a child of the
    <section> element.
    """
    return el('section', *args, **kwargs)


# Text content
def dd(*args, **kwargs):
    """
    The HTML <dd> element (or HTML Description Element) indicates the
    description of a term in a description list (<dl>).
    """
    return el('dd', *args, **kwargs)


def div(*args, **kwargs):
    """
    The HTML <div> element (or HTML Document Division Element) is the
    generic container for flow content, which does not inherently
    represent anything. It can be used to group elements for styling
    purposes (using the class or id attributes), or because they share
    attribute values, such as lang. It should be used only when no
    other semantic element (such as <article> or <nav>) is
    appropriate.
    """
    return el('div', *args, **kwargs)


def dl(*args, **kwargs):
    """
    The HTML <dl> element (or HTML Description List Element) encloses
    a list of groups of terms and descriptions. Common uses for this
    element are to implement a glossary or to display metadata (a list
    of key-value pairs).
    """
    return el('dl', *args, **kwargs)


def dt(*args, **kwargs):
    """
    The HTML <dt> element (or HTML Description Term Element)
    identifies a term in a description list. This element can occur
    only as a child element of a <dl>. It is usually followed by a
    <dd> element; however, multiple <dt> elements in a row indicate
    several terms that are all defined by the immediate next <dd>
    element.
    """
    return el('dt', *args, **kwargs)


def figcaption(*args, **kwargs):
    """
    The HTML <figcaption> element represents a caption or a legend
    associated with a figure or an illustration described by the rest
    of the data of the <figure> element which is its immediate
    ancestor which means <figcaption> can be the first or last element
    inside a <figure> block. Also, the HTML Figcaption Element is
    optional; if not provided, then the parent figure element will
    have no caption.
    """
    return el('figcaption', *args, **kwargs)


def figure(*args, **kwargs):
    """
    The HTML <figure> element represents self-contained content,
    frequently with a caption (<figcaption>), and is typically
    referenced as a single unit. While it is related to the main flow,
    its position is independent of the main flow. Usually this is an
    image, an illustration, a diagram, a code snippet, or a schema
    that is referenced in the main text, but that can be moved to
    another page or to an appendix without affecting the main flow.
    """
    return el('figure', *args, **kwargs)


def hr(*args, **kwargs):
    """
    The HTML <hr> element represents a thematic break between
    paragraph-level elements (for example, a change of scene in a
    story, or a shift of topic with a section). In previous versions
    of HTML, it represented a horizontal rule. It may still be
    displayed as a horizontal rule in visual browsers, but is now
    defined in semantic terms, rather than presentational terms.
    """
    return void_el('hr', *args, **kwargs)


def li(*args, **kwargs):
    """
    The HTML <li> element (or HTML List Item Element) is used to
    represent an item in a list. It must be contained in a parent
    element: an ordered list (<ol>), an unordered list (<ul>), or a
    menu (<menu>). In menus and unordered lists, list items are
    usually displayed using bullet points. In ordered lists, they are
    usually displayed with an ascending counter on the left, such as a
    number or letter.
    """
    return el('li', *args, **kwargs)


def main(*args, **kwargs):
    """
    The HTML <main> element represents the main content of the <body>
    of a document or application. The main content area consists of
    content that is directly related to, or expands upon the central
    topic of a document or the central functionality of an
    application. This content should be unique to the document,
    excluding any content that is repeated across a set of documents
    such as sidebars, navigation links, copyright information, site
    logos, and search forms (unless the document's main function is as
    a search form).
    """
    return el('main', *args, **kwargs)


def ol(*args, **kwargs):
    """
    The HTML <ol> Element (or HTML Ordered List Element) represents an
    ordered list of items. Typically, ordered-list items are displayed
    with a preceding numbering, which can be of any form, like
    numerals, letters or Romans numerals or even simple bullets. This
    numbered style is not defined in the HTML description of the page,
    but in its associated CSS, using the list-style-type property.
    """
    return el('ol', *args, **kwargs)


def p(*args, **kwargs):
    """
    The HTML <p> element (or HTML Paragraph Element) represents a
    paragraph of text.
    """
    return el('p', *args, **kwargs)


def pre(*args, **kwargs):
    """
    The HTML <pre> element (or HTML Preformatted Text) represents
    preformatted text. Text within this element is typically displayed
    in a non-proportional ("monospace") font exactly as it is laid out
    in the file. Whitespace inside this element is displayed as typed.
    """
    return el('pre', *args, **kwargs)


def ul(*args, **kwargs):
    """
    The HTML <ul> element (or HTML Unordered List Element) represents
    an unordered list of items, namely a collection of items that do
    not have a numerical ordering, and their order in the list is
    meaningless. Typically, unordered-list items are displayed with a
    bullet, which can be of several forms, like a dot, a circle or a
    squared. The bullet style is not defined in the HTML description
    of the page, but in its associated CSS, using the list-style-type
    property.
    """
    return el('ul', *args, **kwargs)


# Inline text semantics
def a(*args, **kwargs):
    """
    The HTML Anchor Element (<a>) creates a hyperlink to other web
    pages, files, locations within the same page, email addresses, or
    any other URL.
    """
    return el('a', *args, **kwargs)


def abbr(*args, **kwargs):
    """
    The HTML <abbr> element (or HTML Abbreviation Element) represents
    an abbreviation and optionally provides a full description for
    it. If present, the title attribute must contain this full
    description and nothing else.
    """
    return el('abbr', *args, **kwargs)


def b(*args, **kwargs):
    """
    The HTML <b> Element represents a span of text stylistically
    different from normal text, without conveying any special
    importance or relevance. It is typically used for keywords in a
    summary, product names in a review, or other spans of text whose
    typical presentation would be boldfaced. Another example of its
    use is to mark the lead sentence of each paragraph of an article.
    """
    return el('b', *args, **kwargs)


def bdi(*args, **kwargs):
    """
    The HTML <bdi> Element (or Bi-Directional Isolation Element)
    isolates a span of text that might be formatted in a different
    direction from other text outside it.
    """
    return el('bdi', *args, **kwargs)


def bdo(*args, **kwargs):
    """
    The HTML <bdo> Element (or HTML bidirectional override element) is
    used to override the current directionality of text. It causes the
    directionality of the characters to be ignored in favor of the
    specified directionality.
    """
    return el('bdo', *args, **kwargs)


def br(*args, **kwargs):
    """
    The HTML element line break <br> produces a line break in text
    (carriage-return). It is useful for writing a poem or an address,
    where the division of lines is significant.
    """
    return void_el('br', *args, **kwargs)


def cite(*args, **kwargs):
    """
    The HTML Citation Element (<cite>) represents a reference to a
    creative work. It must include the title of a work or a URL
    reference, which may be in an abbreviated form according to the
    conventions used for the addition of citation metadata.
    """
    return el('cite', *args, **kwargs)


def code(*args, **kwargs):
    """
    The HTML Code Element (<code>) represents a fragment of computer
    code. By default, it is displayed in the browser's default
    monospace font.
    """
    return el('code', *args, **kwargs)


def data(*args, **kwargs):
    """
    The HTML <data> Element links a given content with a
    machine-readable translation. If the content is time- or
    date-related, the <time> must be used.
    """
    return el('data', *args, **kwargs)


def dfn(*args, **kwargs):
    """
    The HTML Definition Element (<dfn>) represents the defining
    instance of a term.
    """
    return el('dfn', *args, **kwargs)


def em(*args, **kwargs):
    """
    The HTML element emphasis <em> marks text that has stress
    emphasis. The <em> element can be nested, with each level of
    nesting indicating a greater degree of emphasis.
    """
    return el('em', *args, **kwargs)


def i(*args, **kwargs):
    """
    The HTML <i> Element represents a range of text that is set off
    from the normal text for some reason, for example, technical
    terms, foreign language phrases, or fictional character
    thoughts. It is typically displayed in italic type.
    """
    return el('i', *args, **kwargs)


def kbd(*args, **kwargs):
    """
    The HTML Keyboard Input Element (<kbd>) represents user input and
    produces an inline element displayed in the browser's default
    monospace font.
    """
    return el('kbd', *args, **kwargs)


def mark(*args, **kwargs):
    """
    The HTML Mark Element (<mark>) represents highlighted text, i.e.,
    a run of text marked for reference purpose, due to its relevance
    in a particular context. For example it can be used in a page
    showing search results to highlight every instance of the
    searched-for word.
    """
    return el('mark', *args, **kwargs)


def q(*args, **kwargs):
    """
    The HTML Quote Element (<q>) indicates that the enclosed text is a
    short inline quotation. This element is intended for short
    quotations that don't require paragraph breaks; for long
    quotations use the <blockquote> element.
    """
    return el('q', *args, **kwargs)


def rp(*args, **kwargs):
    """
    The HTML <rp> element is used to provide fall-back parenthesis for
    browsers non-supporting ruby annotations. Ruby annotations are for
    showing pronunciation of East Asian characters, like using
    Japanese furigana or Taiwainese bopomofo characters. The <rp>
    element is used in the case of lack of <ruby> element support its
    content has what should be displayed in order to indicate the
    presence of a ruby annotation, usually parentheses.
    """
    return el('rp', *args, **kwargs)


def rt(*args, **kwargs):
    """
    The HTML <rt> Element embraces pronunciation of characters
    presented in a ruby annotations, which are used to describe the
    pronunciation of East Asian characters. This element is always
    used inside a <ruby> element.
    """
    return el('rt', *args, **kwargs)


def rtc(*args, **kwargs):
    """
    The HTML <rtc> Element embraces semantic annotations of characters
    presented in a ruby of <rb> elements used inside of <ruby>
    element. <rb> elements can have both pronunciation (<rt>) and
    semantic (<rtc>) annotations.
    """
    return el('rtc', *args, **kwargs)


def ruby(*args, **kwargs):
    """
    The HTML <ruby> Element represents a ruby annotation. Ruby
    annotations are for showing pronunciation of East Asian
    characters.
    """
    return el('ruby', *args, **kwargs)


def s(*args, **kwargs):
    """
    The HTML Strikethrough Element (<s>) renders text with a
    strikethrough, or a line through it. Use the <s> element to
    represent things that are no longer relevant or no longer
    accurate. However, <s> is not appropriate when indicating document
    edits; for that, use the <del> and <ins> elements, as appropriate.
    """
    return el('s', *args, **kwargs)


def samp(*args, **kwargs):
    """
    The HTML <samp> element is an element intended to identify sample
    output from a computer program. It is usually displayed in the
    browser's default monotype font (such as Lucida Console).
    """
    return el('samp', *args, **kwargs)


def small(*args, **kwargs):
    """
    The HTML Small Element (<small>) makes the text font size one size
    smaller (for example, from large to medium, or from small to
    x-small) down to the browser's minimum font size.  In HTML5, this
    element is repurposed to represent side-comments and small print,
    including copyright and legal text, independent of its styled
    presentation.
    """
    return el('small', *args, **kwargs)


def span(*args, **kwargs):
    """
    The HTML <span> element is a generic inline container for phrasing
    content, which does not inherently represent anything. It can be
    used to group elements for styling purposes (using the class or id
    attributes), or because they share attribute values, such as lang.
    """
    return el('span', *args, **kwargs)


def strong(*args, **kwargs):
    """
    The HTML <strong> element (or HTML Strong Element) gives text
    strong importance, and is typically displayed in bold.
    """
    return el('strong', *args, **kwargs)


def sub(*args, **kwargs):
    """
    The HTML Subscript Element (<sub>) defines a span of text that
    should be displayed, for typographic reasons, lower, and often
    smaller, than the main span of text.
    """
    return el('sub', *args, **kwargs)


def sup(*args, **kwargs):
    """
    The HTML Superscript Element (<sup>) defines a span of text that
    should be displayed, for typographic reasons, higher, and often
    smaller, than the main span of text.
    """
    return el('sup', *args, **kwargs)


def time(*args, **kwargs):
    """
    The HTML <time> element represents either a time on a 24-hour
    clock or a precise date in the Gregorian calendar (with optional
    time and timezone information).
    """
    return el('time', *args, **kwargs)


def u(*args, **kwargs):
    """
    The HTML Underline Element (<u>) renders text with an underline, a
    line under the baseline of its content.
    """
    return el('u', *args, **kwargs)


def var(*args, **kwargs):
    """
    The HTML Variable Element (<var>) represents a variable in a
    mathematical expression or a programming context.
    """
    return el('var', *args, **kwargs)


def wbr(*args, **kwargs):
    """
    The HTML element word break opportunity <wbr> represents a
    position within text where the browser may optionally break a
    line, though its line-breaking rules would not otherwise create a
    break at that location.
    """
    return el('wbr', *args, **kwargs)


# Image and multimedia
def area(*args, **kwargs):
    """
    The HTML <area> element defines a hot-spot region on an image, and
    optionally associates it with a hypertext link. This element is
    used only within a <map> element.
    """
    return void_el('area', *args, **kwargs)


def audio(*args, **kwargs):
    """
    The HTML <audio> element is used to embed sound content in
    documents. It may contain one or more audio sources, represented
    using the src attribute or the <source> element; the browser will
    choose the most suitable one.
    """
    return el('audio', *args, **kwargs)


def img(*args, **kwargs):
    """
    The HTML <img> element represents an image in the document.
    """
    return void_el('img', *args, **kwargs)


def map(*args, **kwargs):
    """
    The HTML <map> element is used with <area> elements to define an
    image map (a clickable link area).
    """
    return el('map', *args, **kwargs)


def track(*args, **kwargs):
    """
    The HTML <track> element is used as a child of the media
    elements—<audio> and <video>. It lets you specify timed text
    tracks (or time-based data), for example to automatically handle
    subtitles. The tracks are formatted in WebVTT format (.vtt files)
    — Web Video Text Tracks.
    """
    return el('track', *args, **kwargs)


def video(*args, **kwargs):
    """
    Use the HTML <video> element to embed video content in a
    document. The video element contains one or more video sources. To
    specify a video source, use either the src attribute or the
    <source> element; the browser will choose the most suitable one.
    """
    return el('video', *args, **kwargs)


# Embedded content
def embed(*args, **kwargs):
    """
    The HTML <embed> Element represents an integration point for an
    external application or interactive content (in other words, a
    plug-in).
    """
    return el('embed', *args, **kwargs)


def object(*args, **kwargs):
    """
    The HTML Embedded Object Element (<object>) represents an external
    resource, which can be treated as an image, a nested browsing
    context, or a resource to be handled by a plugin.
    """
    return el('object', *args, **kwargs)


def param(*args, **kwargs):
    """
    The HTML <param> Element (or HTML Parameter Element) defines
    parameters for <object>.
    """
    return void_el('param', *args, **kwargs)


def source(*args, **kwargs):
    """
    The HTML <source> element specifies multiple media resources for
    either the <picture>, the <audio> or the <video> element. It is an
    empty element. It is commonly used to serve the same media content
    in multiple formats supported by different browsers.
    """
    return el('source', *args, **kwargs)


# Scripting
def canvas(*args, **kwargs):
    """
    The HTML <canvas> Element can be used to draw graphics via
    scripting (usually JavaScript). For example, it can be used to
    draw graphs, make photo compositions or even perform
    animations. You may (and should) provide alternate content inside
    the <canvas> block. That content will be rendered both on older
    browsers that don't support canvas and in browsers with JavaScript
    disabled.
    """
    return el('canvas', *args, **kwargs)


def noscript(*args, **kwargs):
    """
    The HTML <noscript> Element defines a section of html to be
    inserted if a script type on the page is unsupported or if
    scripting is currently turned off in the browser.
    """
    return el('noscript', *args, **kwargs)


def script(*args, **kwargs):
    """
    The <script> element (or HTML Script Element ) is used to embed or
    reference an executable script within an HTML or XHTML document.
    """
    return el('script', *args, **kwargs)


# Demarcating edits
def del_(*args, **kwargs):
    """
    The HTML Deleted Text Element (<del>) represents a range of text
    that has been deleted from a document. This element is often (but
    need not be) rendered with strike-through text.
    Added underscore is needed to avoid conflict with python resrved word.
    """
    return el('del', *args, **kwargs)


def ins(*args, **kwargs):
    """
    The HTML <ins> Element (or HTML Inserted Text) HTML represents a
    range of text that has been added to a document.
    """
    return el('ins', *args, **kwargs)


# Table content
def caption(*args, **kwargs):
    """
    The HTML <caption> Element (or HTML Table Caption Element)
    represents the title of a table. Though it is always the first
    descendant of a <table>, its styling, using CSS, may place it
    elsewhere, relative to the table.
    """
    return el('caption', *args, **kwargs)


def col(*args, **kwargs):
    """
    The HTML Table Column Element (<col>) defines a column within a
    table and is used for defining common semantics on all common
    cells. It is generally found within a <colgroup> element.
    """
    return void_el('col', *args, **kwargs)


def colgroup(*args, **kwargs):
    """
    The HTML Table Column Group Element (<colgroup>) defines a group
    of columns within a table.
    """
    return el('colgroup', *args, **kwargs)


def table(*args, **kwargs):
    """
    The HTML Table Element (<table>) represents tabular data - i.e.,
    information expressed via a two dimensional data table.
    """
    return el('table', *args, **kwargs)


def tbody(*args, **kwargs):
    """
    The HTML Table Body Element (<tbody>) defines one or more <tr>
    element data-rows to be the body of its parent <table> element (as
    long as no <tr> elements are immediate children of that table
    element.)  In conjunction with a preceding <thead> and/or <tfoot>
    element, <tbody> provides additional semantic information for
    devices such as printers and displays. Of the parent table's child
    elements, <tbody> represents the content which, when longer than a
    page, will most likely differ for each page printed; while the
    content of <thead> and <tfoot> will be the same or similar for
    each page printed. For displays, <tbody> will enable separate
    scrolling of the <thead>, <tfoot>, and <caption> elements of the
    same parent <table> element.  Note that unlike the <thead>,
    <tfoot>, and <caption> elements however, multiple <tbody> elements
    are permitted (if consecutive), allowing the data-rows in long
    tables to be divided into different sections, each separately
    formatted as needed.
    """
    return el('tbody', *args, **kwargs)


def td(*args, **kwargs):
    """
    The Table cell HTML element (<td>) defines a cell of a table that
    contains data. It participates in the table model.
    """
    return el('td', *args, **kwargs)


def tfoot(*args, **kwargs):
    """
    The HTML Table Foot Element (<tfoot>) defines a set of rows
    summarizing the columns of the table.
    """
    return el('tfoot', *args, **kwargs)


def th(*args, **kwargs):
    """
    The HTML element table header cell <th> defines a cell as header
    of a group of table cells. The exact nature of this group is
    defined by the scope and headers attributes.
    """
    return el('th', *args, **kwargs)


def thead(*args, **kwargs):
    """
    The HTML Table Head Element (<thead>) defines a set of rows
    defining the head of the columns of the table.
    """
    return el('thead', *args, **kwargs)


def tr(*args, **kwargs):
    """
    The HTML element table row <tr> defines a row of cells in a
    table. Those can be a mix of <td> and <th> elements.
    """
    return el('tr', *args, **kwargs)


# Forms
def button(*args, **kwargs):
    """
    The HTML <button> Element represents a clickable button.
    """
    return el('button', *args, **kwargs)


def datalist(*args, **kwargs):
    """
    The HTML Datalist Element (<datalist>) contains a set of <option>
    elements that represent the values available for other controls.
    """
    return el('datalist', *args, **kwargs)


def fieldset(*args, **kwargs):
    """
    The HTML <fieldset> element is used to group several controls as
    well as labels (<label>) within a web form.
    """
    return el('fieldset', *args, **kwargs)


def form(*args, **kwargs):
    """
    The HTML <form> element represents a document section that
    contains interactive controls to submit information to a web
    server.
    """
    return el('form', *args, **kwargs)


def input(*args, **kwargs):
    """
    The HTML element <input> is used to create interactive controls
    for web-based forms in order to accept data from the user. How an
    <input> works varies considerably depending on the value of its
    type attribute.
    """
    return void_el('input', *args, **kwargs)


def label(*args, **kwargs):
    """
    The HTML Label Element (<label>) represents a caption for an item
    in a user interface. It can be associated with a control either by
    placing the control element inside the <label> element, or by
    using the for attribute. Such a control is called the labeled
    control of the label element. One input can be associated with
    multiple labels.
    """
    return el('label', *args, **kwargs)


def legend(*args, **kwargs):
    """
    The HTML <legend> Element (or HTML Legend Field Element)
    represents a caption for the content of its parent <fieldset>.
    """
    return el('legend', *args, **kwargs)


def meter(*args, **kwargs):
    """
    The HTML <meter> Element represents either a scalar value within a
    known range or a fractional value.
    """
    return el('meter', *args, **kwargs)


def optgroup(*args, **kwargs):
    """
    In a Web form, the HTML <optgroup> element creates a grouping of
    options within a <select> element.
    """
    return el('optgroup', *args, **kwargs)


def option(*args, **kwargs):
    """
    In a Web form, the HTML <option> element is used to create a
    control representing an item within a <select>, an <optgroup> or a
    <datalist> HTML5 element.
    """
    return el('option', *args, **kwargs)


def output(*args, **kwargs):
    """
    The HTML <output> element represents the result of a calculation
    or user action.
    """
    return el('output', *args, **kwargs)


def progress(*args, **kwargs):
    """
    The HTML <progress> Element is used to view the completion
    progress of a task. While the specifics of how it's displayed is
    left up to the browser developer, it's typically displayed as a
    progress bar. Javascript can be used to manipulate the value of
    progress bar.
    """
    return el('progress', *args, **kwargs)


def select(*args, **kwargs):
    """
    The HTML select (<select>) element represents a control that
    presents a menu of options. The options within the menu are
    represented by <option> elements, which can be grouped by
    <optgroup> elements. Options can be pre-selected for the user.
    """
    return el('select', *args, **kwargs)


def textarea(*args, **kwargs):
    """
    The HTML <textarea> element represents a multi-line plain-text
    editing control.
    """
    return el('textarea', *args, **kwargs)


# Interactive elements
def details(*args, **kwargs):
    """
    The HTML <details> element is used as a disclosure widget from
    which the user can retrieve additional information.
    """
    return el('details', *args, **kwargs)


def dialog(*args, **kwargs):
    """
    The HTML <dialog> element represents a dialog box or other
    interactive component, such as an inspector or window. <form>
    elements can be integrated within a dialog by specifying them with
    the attribute method="dialog". When such a form is submitted, the
    dialog is closed with a returnValue attribute set to the value of
    the submit button used.
    """
    return el('dialog', *args, **kwargs)


def menu(*args, **kwargs):
    """
    The HTML <menu> element represents a group of commands that a user
    can perform or activate. This includes both list menus, which
    might appear across the top of a screen, as well as context menus,
    such as those that might appear underneath a button after it has
    been clicked.
    """
    return el('menu', *args, **kwargs)


def menuitem(*args, **kwargs):
    """
    The HTML <menuitem> element represents a command that a user is
    able to invoke through a popup menu. This includes context menus,
    as well as menus that might be attached to a menu button.
    """
    return el('menuitem', *args, **kwargs)


def summary(*args, **kwargs):
    """
    The HTML <summary> element is used as a summary, caption, or
    legend for the content of a <details> element.
    """
    return el('summary', *args, **kwargs)


# Web Components
def content(*args, **kwargs):
    """
    The HTML <content> element is used inside of Shadow DOM as an
    insertion point. It is not intended to be used in ordinary
    HTML. It is used with Web Components. It has now been replaced by
    the <slot> element.
    """
    return el('content', *args, **kwargs)


def element(*args, **kwargs):
    """
    The HTML <element> element is used to define new custom DOM
    elements.
    """
    return el('element', *args, **kwargs)


def shadow(*args, **kwargs):
    """
    The HTML <shadow> element is used as a shadow DOM insertion
    point. You might use it if you have created multiple shadow roots
    under a shadow host. It is not useful in ordinary HTML. It is used
    with Web Components.
    """
    return el('shadow', *args, **kwargs)


def template(*args, **kwargs):
    """
    The HTML template element <template> is a mechanism for holding
    client-side content that is not to be rendered when a page is
    loaded but may subsequently be instantiated during runtime using
    JavaScript.
    """
    return el('template', *args, **kwargs)
